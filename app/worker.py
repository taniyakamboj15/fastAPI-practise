import time
import random
from celery import Task
from app.core.celery_app import celery_app

@celery_app.task(acks_late=True)
def long_running_task(word: str) -> str:
    """
    Simulates a heavy task (e.g., video processing).
    """
    time.sleep(5)
    return f"Processed: {word}"

@celery_app.task(
    bind=True,
    acks_late=True,
    autoretry_for=(ValueError,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5}
)
def task_with_retry(self, input_data: str):
    """
    Simulates a flaky task that might fail (e.g., external API call).
    Retries automatically on ValueError.
    """
    if random.choice([True, False]):
        print(f"Task Failed! Retrying... (Input: {input_data})")
        raise ValueError("Simulated network failure!")
    
    return f"Success: {input_data}"

@celery_app.task
def scheduled_task_demo():
    print("CRON JOB EXECUTED: I run every minute!")
