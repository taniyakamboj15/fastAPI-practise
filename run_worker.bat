@echo off
echo Starting Celery Worker...
echo Press Ctrl+C to stop.
.\venv\Scripts\celery -A app.core.celery_app worker --loglevel=info --pool=solo
pause
