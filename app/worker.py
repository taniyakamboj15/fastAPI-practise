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

@celery_app.task(bind=True)
def process_order(self, order_id: str):
    """
    Idempotent task: Processes an order ONLY if it hasn't been processed before.
    Uses Redis atomic 'setnx' (Set if Not eXists).
    """
    # Access the Redis client from the Celery backend
    # This works because we are using Redis as the result backend
    redis_client = self.backend.client

    key = f"order:{order_id}:processed"

    # Try to set the key. Returns True if set, False if already existed.
    if redis_client.setnx(key, "1"):
        # We acquired the lock -> Process the order
        print(f"PROCESSING ORDER: {order_id}...")
        time.sleep(4) # Simulate payment processing
        return f"Order {order_id} Processed Successfully"
    else:
        # Lock failed -> Already processed
        print(f"IGNORING ORDER: {order_id} (Duplicate Received)")
        return f"Order {order_id} Skipped (Idempotent)"
