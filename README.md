# BlazeNXT - Enterprise OTP Dashboard

This repository contains the backend and dashboard interface for the BlazeNXT Enterprise OTP System, inspired by the minimalist terminal aesthetic of `infinity-sms.vercel.app`.

## Features
- **LIVE OTP Feed**: Real-time SMS interception terminal.
- **Cyberpunk UI**: CRT flicker effects, high contrast neon-on-black terminal design.
- **SPA with URL Routing**: Fast dynamic single page application supporting direct URL navigation (`/otp`, `/numbers`, `/api`).
- **Auto-Copy & Sound**: Browser notifications and auto-clipboard copying of incoming intercepts.
- **Railway Deployment Ready**: Natively exposes ports and integrates securely with Railway.app variable configurations.

## Railway.app Deployment
This app is ready to deploy on [Railway](https://railway.app/). 
Railway will automatically detect the `Procfile` and use `start.sh` to run **both** the Flask Dashboard and the Telegram Bot concurrently.

### Required Railway Environment Variables
When setting up the project on Railway, configure the following variables in the **Variables** tab:

```env
BOT_TOKEN=your_telegram_bot_token
OWNER_IDS=123456789,987654321
ADMIN_IDS=123456789,987654321
OTP_GROUP_LINK=https://t.me/+YourGroup
BOT_NAME=BlazeNXT OTP Bot
DEV_CONTACT=@your_telegram_username
OTP_GROUP_IDS=-1003902733109
DASHBOARD_PASS=admin
DASHBOARD_SECRET=your_super_secret_jwt_key
PORT=8080
```

> **Note**: Railway will usually assign `PORT` automatically, but you can explicitly specify it.

## Files
- `app.py`: The Telegram Bot daemon, which manages OTP processing and queues.
- `dashboard.py`: Flask-based REST API and backend serving data to the web dashboard.
- `dashboard.html`: Single-page application containing the admin interface for data visualization.
- `start.sh`: Shell executable to run both services.
- `Procfile`: Entry point declaration for production environments like Railway.
