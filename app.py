import os
import threading
from flask import Flask, render_template_string
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
PORT = int(os.environ.get("PORT", 8000))

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    users[user_id] = {
        "full_name": user.full_name,
        "username": user.username
    }
    await update.message.reply_text(f"Hello {user.full_name}! Your info has been saved.")

app_web = Flask(__name__)

@app_web.route("/")
def dashboard():
    html = """
    <h1>Telegram Bot Users Dashboard</h1>
    <table border="1">
        <tr><th>User ID</th><th>Full Name</th><th>Username</th></tr>
        {% for user_id, info in users.items() %}
        <tr>
            <td>{{ user_id }}</td>
            <td>{{ info.full_name }}</td>
            <td>{{ info.username }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, users=users)

def run_bot():
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN not set — bot polling skipped.")
        return
    print("Bot is running...")
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    print(f"Web dashboard running on http://127.0.0.1:{PORT}")
    app_web.run(host="0.0.0.0", port=PORT, debug=False)
