#!/bin/bash

# Trap SIGTERM to gracefully shut down the child processes (Prevents Telegram Polling Conflict on Railway Deploy)
trap 'kill $GUNICORN_PID $BOT_PID; exit' SIGTERM SIGINT

echo "Starting Flask Dashboard..."
gunicorn -b 0.0.0.0:${PORT:-8080} dashboard:app &
GUNICORN_PID=$!

echo "Starting Telegram Bot..."
while true; do
    python app.py &
    BOT_PID=$!
    wait $BOT_PID
    echo "Bot crashed! Restarting in 5 seconds..."
    sleep 5
done &

wait $GUNICORN_PID
