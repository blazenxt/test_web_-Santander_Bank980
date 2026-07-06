#!/bin/bash

# Start the Flask dashboard via Gunicorn in the background
echo "Starting Flask Dashboard..."
gunicorn -b 0.0.0.0:${PORT:-8080} dashboard:app &

# Start the Telegram Bot in the foreground
echo "Starting Telegram Bot..."
python app.py
