from taskiq import TaskiqScheduler
import taskiq_fastapi
from taskiq_redis import RedisStreamBroker, RedisAsyncResultBackend
from taskiq.schedule_sources import LabelScheduleSource

from src.config import settings

result_backend = RedisAsyncResultBackend(settings.REDIS_URL)

broker = RedisStreamBroker(url=settings.REDIS_URL)
broker = broker.with_result_backend(result_backend)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

taskiq_fastapi.init(broker, "src.main:app")