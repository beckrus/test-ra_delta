from taskiq import InMemoryBroker, TaskiqScheduler
import taskiq_fastapi
from taskiq.schedule_sources import LabelScheduleSource


# result_backend = RedisAsyncResultBackend(settings.REDIS_URL)

# broker = RedisStreamBroker(url=settings.REDIS_URL)

# broker = broker.with_result_backend(result_backend)

# if settings.MODE == "TEST":
#     broker = InMemoryBroker()

broker = InMemoryBroker()

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

taskiq_fastapi.init(broker, "src.main:app")
