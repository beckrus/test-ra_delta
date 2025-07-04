import json
import logging
from typing import Optional
import httpx
import redis.asyncio as aioredis
from src.config import settings

logger = logging.getLogger(__name__)

class ExchangeRateService:
    """Get exchange rate from cbr-xml-daily.ru (async, with Redis cache)"""

    def __init__(self):
        self.redis_client: Optional[aioredis.Redis] = None
        self.cbr_api_url = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.cache_key = "usd_to_rub_rate"
        self.cache_ttl = 3600

    async def get_redis_client(self) -> aioredis.Redis:
        if self.redis_client is None:
            self.redis_client = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
        return self.redis_client

    async def get_usd_to_rub_rate(self) -> float:
        try:
            cached_rate = await self._get_cached_rate()
            if cached_rate is not None:
                logger.info(f"Rate from cache USD/RUB: {cached_rate}")
                return cached_rate

            rate = await self._fetch_rate_from_api()
            await self._cache_rate(rate)
            logger.info(f"New rate for USD/RUB: {rate}")
            return rate

        except Exception as e:
            logger.error(f"Can't get rate: {e}")
            raise

    async def _get_cached_rate(self) -> Optional[float]:
        try:
            redis_client = await self.get_redis_client()
            cached_value = await redis_client.get(self.cache_key)
            if cached_value:
                return float(cached_value)
            return None
        except Exception as e:
            logger.error(f"Can't read from Redis: {e}")
            return None

    async def _cache_rate(self, rate: float) -> None:
        try:
            redis_client = await self.get_redis_client()
            await redis_client.setex(
                self.cache_key,
                self.cache_ttl,
                str(rate)
            )
            logger.info(f"Rate {rate} saved in cache for {self.cache_ttl}s")
        except Exception as e:
            logger.error(f"Can't write to Redis: {e}")

    async def _fetch_rate_from_api(self) -> float:
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(self.cbr_api_url)
                response.raise_for_status()
                data = response.json()
                usd_data = data.get("Valute", {}).get("USD", {})
                if not usd_data:
                    raise ValueError("No USD data")
                rate = float(usd_data.get("Value", 0))
                if rate <= 0:
                    raise ValueError(f"Incorrect rate for USD: {rate}")
                return rate
            except httpx.RequestError as e:
                logger.error(f"HTTP request error API ЦБ РФ: {e}")
                raise
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                logger.error(f"Parsing error API ЦБ РФ: {e}")
                raise

exchange_service = ExchangeRateService()

async def get_current_usd_rate() -> float:
    return await exchange_service.get_usd_to_rub_rate()