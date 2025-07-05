from taskiq import InMemoryBroker, TaskiqScheduler
import taskiq_fastapi
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker
from src.config import settings

result_backend = RedisAsyncResultBackend(settings.REDIS_URL)

broker = RedisStreamBroker(url=settings.REDIS_URL)

broker = broker.with_result_backend(result_backend)

if settings.MODE == "TEST":
    broker = InMemoryBroker()


scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

taskiq_fastapi.init(broker, "src.main:app")
