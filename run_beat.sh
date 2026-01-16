#!/bin/bash
echo "Starting Celery Beat (Scheduler)..."
./venv/bin/celery -A app.core.celery_app beat --loglevel=info
