"""
Run this script once after deployment to register the webhook with Telegram.

Usage:
    TELEGRAM_BOT_TOKEN=<your_token> VERCEL_URL=<your_vercel_domain> python setup_webhook.py

Example:
    TELEGRAM_BOT_TOKEN=123456:ABC-DEF VERCEL_URL=your-bot.vercel.app python setup_webhook.py
"""

import asyncio
import os

from telegram import Bot


async def set_webhook():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    vercel_url = os.environ["VERCEL_URL"].rstrip("/")

    webhook_url = f"https://{vercel_url}/api/webhook"

    bot = Bot(token=token)
    result = await bot.set_webhook(url=webhook_url)

    if result:
        info = await bot.get_webhook_info()
        print(f"Webhook set successfully!")
        print(f"URL: {info.url}")
        print(f"Pending updates: {info.pending_update_count}")
    else:
        print("Failed to set webhook.")


asyncio.run(set_webhook())
