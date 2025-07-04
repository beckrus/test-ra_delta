from celery import Celery
from celery.schedules import crontab

from src.config import settings


celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    result_backend=settings.REDIS_URL,
    include=[
        "src.tasks.task_exchange.py",
    ],
)
