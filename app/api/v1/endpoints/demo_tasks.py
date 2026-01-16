from fastapi import APIRouter, BackgroundTasks
import time

from app.worker import long_running_task, task_with_retry

router = APIRouter()

# --- PART 1: FastAPI Native Background Tasks ---

def write_notification(email: str, message: str):
    """
    Simulated background function (no return value needed).
    """
    # Simulate IO delay (e.g., sending email)
    time.sleep(3) 
    print(f"EMAIL SENT TO: {email} | MESSAGE: {message}")

@router.post("/background-simple")
async def send_notification(
    email: str, 
    background_tasks: BackgroundTasks
):
    """
    Demo of Lightweight Background Task.
    Response is sent IMMEDIATELY, email sends later.
    """
    background_tasks.add_task(write_notification, email, message="Welcome to the system!")
    return {"message": "Notification sent in the background"}


# --- PART 2: Celery Distributed Tasks ---

@router.post("/celery-heavy")
async def run_heavy_task(word: str):
    """
    Trigger a heavy Celery task.
    Returns the Task ID immediately.
    """
    task = long_running_task.delay(word)
    return {"message": "Task received", "task_id": task.id}

@router.post("/celery-retry")
async def run_retry_task(word: str):
    """
    Trigger a flaky task to see Retry logic in logs.
    """
    task = task_with_retry.delay(word)
    return {"message": "Retry Task received", "task_id": task.id}
