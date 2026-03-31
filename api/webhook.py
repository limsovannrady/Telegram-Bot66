import asyncio
import json
import os
from http.server import BaseHTTPRequestHandler

from telegram import Update, constants
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    await update.message.reply_text(f"សួស្តី {update.effective_user.first_name}")


async def process_update(update_data: dict):
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    async with application:
        update = Update.de_json(update_data, application.bot)
        await application.process_update(update)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        update_data = json.loads(body.decode("utf-8"))

        asyncio.run(process_update(update_data))

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Webhook is active.")

    def log_message(self, format, *args):
        pass
