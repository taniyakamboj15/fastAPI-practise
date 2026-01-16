#!/bin/bash
echo "Starting Flower Monitoring..."
echo "Access the dashboard at: http://localhost:5555"
./venv/bin/celery -A app.core.celery_app flower
