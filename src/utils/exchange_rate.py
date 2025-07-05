import logging
from abc import ABC, abstractmethod
from typing import Optional
import httpx
import redis.asyncio as aioredis
from src.exceptions import RateCacheError, RateProviderError
from src.config import settings

logger = logging.getLogger(__name__)


class AbstractRateProvider(ABC):
    @abstractmethod
    async def get_rate(self) -> float:
        pass


class AbstractRateCache(ABC):
    @abstractmethod
    async def get(self) -> Optional[float]:
        pass

    @abstractmethod
    async def set(self, value: float) -> None:
        pass


class CBRRateProvider(AbstractRateProvider):
    def __init__(self):
        self.url = "https://www.cbr-xml-daily.ru/daily_json.js"

    async def get_rate(self) -> float:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(self.url)
                resp.raise_for_status()
                data = resp.json()
                usd = data.get("Valute", {}).get("USD")
                if not usd:
                    raise ValueError("Missing 'USD' in Valute")
                rate = float(usd.get("Value", 0))
                if rate <= 0:
                    raise ValueError(f"Incorrect rate for USD: {rate}")
                return rate
        except httpx.HTTPStatusError as e:
            logger.critical(f"[CBRRateProvider] HTTP error: {e.response.status_code}")
            raise RateProviderError("CBR API HTTP error") from e
        except httpx.RequestError as e:
            logger.critical(f"[CBRRateProvider] Request failed: {e}")
            raise RateProviderError("CBR API not reachable") from e
        except Exception as e:
            logger.critical(f"[CBRRateProvider] Parse error: {e}")
            raise RateProviderError("Failed to parse response from CBR API") from e


class RedisRateCache(AbstractRateCache):
    def __init__(self, redis_url: str, key: str = "usd_to_rub_rate", ttl: int = 3600):
        self.redis = aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        self.key = key
        self.ttl = ttl

    async def get(self) -> Optional[float]:
        try:
            val = await self.redis.get(self.key)
            return float(val) if val else None
        except Exception as e:
            logger.warning(f"[RedisRateCache] Failed to read cache: {e}")
            raise RateCacheError("Failed to read from Redis") from e

    async def set(self, value: float) -> None:
        try:
            await self.redis.setex(self.key, self.ttl, str(value))
        except Exception as e:
            logger.warning(f"[RedisRateCache] Failed to write cache: {e}")
            raise RateCacheError("Failed to write to Redis") from e


class ExchangeRateService:
    def __init__(self, provider: AbstractRateProvider, cache: AbstractRateCache):
        self.provider = provider
        self.cache = cache

    async def get_usd_to_rub_rate(self) -> float:
        cached = await self.cache.get()
        if cached:
            logger.info(f"Rate from cache: {cached}")
            return cached

        rate = await self.provider.get_rate()
        await self.cache.set(rate)
        logger.info(f"Fetched rate: {rate}")
        return rate


provider = CBRRateProvider()
cache = RedisRateCache(settings.REDIS_URL)
exchange_service = ExchangeRateService(provider, cache)


async def get_current_usd_rate() -> float:
    return await exchange_service.get_usd_to_rub_rate()
