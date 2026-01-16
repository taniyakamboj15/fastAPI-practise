#!/bin/bash
echo "Starting Celery Worker..."
# Note: Removed --pool=solo which is typically for Windows. Default prefork is better on Mac/Linux.
./venv/bin/celery -A app.core.celery_app worker --loglevel=info
