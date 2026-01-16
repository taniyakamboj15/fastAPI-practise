from celery import Celery
from app.core.config import settings

celery_app = Celery("worker", broker=settings.CELERY_BROKER_URL, include=["app.worker"])

celery_app.conf.update(
    task_track_started=True,
    result_backend=settings.CELERY_RESULT_BACKEND,
)

# Scheduled Tasks (Cron Jobs)
celery_app.conf.beat_schedule = {
    "run-every-30-seconds": {
        "task": "app.worker.scheduled_task_demo",
        "schedule": 30.0, # Run every 30 seconds
    },
}
