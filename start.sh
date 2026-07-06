#!/bin/bash

# Start the Flask dashboard via Gunicorn in the background
echo "Starting Flask Dashboard..."
gunicorn -b 0.0.0.0:${PORT:-8080} dashboard:app &

# Run the Telegram Bot in a while loop so it restarts on crash without killing the container
echo "Starting Telegram Bot..."
while true; do
    python app.py
    echo "Bot crashed! Restarting in 5 seconds..."
    sleep 5
done
