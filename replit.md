# Telegram Bot (Webhook for Vercel)

## Overview

Python-based Telegram bot designed to be deployed on Vercel as a serverless webhook.

## Stack

- **Language**: Python 3.12
- **Library**: python-telegram-bot >= 22.7
- **Deployment**: Vercel (serverless functions)
- **Mode**: Webhook (not polling)

## Project Structure

```
├── api/
│   └── webhook.py       # Vercel serverless function — handles incoming Telegram updates
├── bot.py               # Local development only (long polling)
├── setup_webhook.py     # Run once after deploy to register webhook URL with Telegram
├── vercel.json          # Vercel deployment configuration
├── requirements.txt     # Python dependencies for Vercel
└── pyproject.toml       # Python project config (for local/Replit use)
```

## Environment Variables

| Variable            | Description                        |
|---------------------|------------------------------------|
| `TELEGRAM_BOT_TOKEN`| Your Telegram bot token from @BotFather |

## Deployment Steps (Vercel)

1. Push code to GitHub
2. Import project in Vercel dashboard
3. Add `TELEGRAM_BOT_TOKEN` as an Environment Variable in Vercel
4. Deploy
5. After deployment, run `setup_webhook.py` to register the webhook:

```bash
TELEGRAM_BOT_TOKEN=<token> VERCEL_URL=<your-domain.vercel.app> python setup_webhook.py
```

## Local Development

Use `bot.py` with long polling for local testing:

```bash
python bot.py
```

## Webhook Endpoint

```
POST https://<your-domain>.vercel.app/api/webhook
```

Telegram will send all bot updates to this URL.
