@echo off
echo Starting Celery Beat (Scheduler)...
echo Press Ctrl+C to stop.
.\venv\Scripts\celery -A app.core.celery_app beat --loglevel=info
pause
