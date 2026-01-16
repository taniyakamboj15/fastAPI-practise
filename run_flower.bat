@echo off
echo Starting Flower Monitoring...
echo Access the dashboard at: http://localhost:5555
echo Press Ctrl+C to stop.
.\venv\Scripts\celery -A app.core.celery_app flower
pause
