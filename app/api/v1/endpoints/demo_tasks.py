from fastapi import APIRouter, BackgroundTasks
import time

from app.worker import long_running_task, task_with_retry

router = APIRouter()


def write_notification(email: str, message: str):

    time.sleep(3) 
    print(f"EMAIL SENT TO: {email} | MESSAGE: {message}")

@router.post("/background-simple")
async def send_notification(
    email: str, 
    background_tasks: BackgroundTasks
):
  
    background_tasks.add_task(write_notification, email, message="Welcome to the system!")
    return {"message": "Notification sent in the background"}



@router.post("/celery-heavy")
async def run_heavy_task(word: str):
   
    task = long_running_task.delay(word)
    return {"message": "Task received", "task_id": task.id}

@router.post("/celery-retry")
async def run_retry_task(word: str):
  
    task = task_with_retry.delay(word)
    return {"message": "Retry Task received", "task_id": task.id}

@router.post("/celery-order")
async def run_order_task(order_id: str):

    from app.worker import process_order 
    
    task = process_order.delay(order_id)
    return {
        "message": "Order Task Submitted", 
        "task_id": task.id, 
        "order_id": order_id,
        "hint": "Check Worker logs to see if it processes or skips!"
    }
