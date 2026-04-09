# Telegram Bot

## Overview

Python-based Telegram bot running on Replit using long polling.

## Stack

- **Language**: Python 3.11+
- **Library**: python-telegram-bot == 22.7
- **Mode**: Long polling (runs continuously on Replit)

## Project Structure

```
├── bot.py               # Main entry point — runs the bot with long polling
├── api/
│   └── webhook.py       # Legacy Vercel webhook handler (not used on Replit)
├── setup_webhook.py     # Utility to register webhook URL (not needed for polling mode)
├── requirements.txt     # Python dependencies
└── pyproject.toml       # Python project config
```

## Environment Variables / Secrets

| Variable             | Description                                 |
|----------------------|---------------------------------------------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from @BotFather     |

Set this via the Replit Secrets tab (the padlock icon in the sidebar).

## Running the Bot

The bot runs automatically via the "Telegram Bot" workflow, which executes:

```bash
python3 bot.py
```

It will connect to Telegram and respond to the `/start` command with a greeting in Khmer.

## Bot Commands

- `/start` — Replies with "សួស្តី [Your Name]"
