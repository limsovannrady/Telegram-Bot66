import os
import asyncio
import threading
from flask import Flask, render_template_string
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
PORT = int(os.environ.get("BOT_PORT", 3001))

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users[user.id] = {
        "full_name": user.full_name,
        "username": user.username or "—",
    }
    await update.message.reply_text(f"សួស្តី {user.full_name}! ព័ត៌មានរបស់អ្នកត្រូវបានរក្សាទុក។")

app_web = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="km">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Telegram Bot Dashboard</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #f0f4f8;
      color: #1a202c;
      min-height: 100vh;
    }
    header {
      background: linear-gradient(135deg, #0088cc, #005f99);
      color: white;
      padding: 24px 32px;
      display: flex;
      align-items: center;
      gap: 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    header svg { flex-shrink: 0; }
    header h1 { font-size: 1.5rem; font-weight: 700; }
    header p { font-size: 0.875rem; opacity: 0.85; margin-top: 2px; }
    .container { max-width: 900px; margin: 40px auto; padding: 0 20px; }
    .stats {
      display: flex;
      gap: 16px;
      margin-bottom: 28px;
    }
    .stat-card {
      background: white;
      border-radius: 12px;
      padding: 20px 28px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
      flex: 1;
    }
    .stat-card .label { font-size: 0.8rem; color: #718096; text-transform: uppercase; letter-spacing: 0.05em; }
    .stat-card .value { font-size: 2rem; font-weight: 700; color: #0088cc; margin-top: 4px; }
    .card {
      background: white;
      border-radius: 12px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
      overflow: hidden;
    }
    .card-header {
      padding: 18px 24px;
      border-bottom: 1px solid #e2e8f0;
      font-weight: 600;
      font-size: 0.95rem;
      color: #2d3748;
    }
    table { width: 100%; border-collapse: collapse; }
    th {
      background: #f7fafc;
      padding: 12px 20px;
      text-align: left;
      font-size: 0.78rem;
      font-weight: 600;
      color: #718096;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    td {
      padding: 14px 20px;
      font-size: 0.9rem;
      border-top: 1px solid #edf2f7;
      vertical-align: middle;
    }
    tr:hover td { background: #f7fafc; }
    .badge {
      display: inline-block;
      background: #ebf8ff;
      color: #0088cc;
      padding: 2px 10px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 500;
    }
    .empty {
      text-align: center;
      padding: 60px 20px;
      color: #a0aec0;
    }
    .empty svg { margin-bottom: 12px; opacity: 0.4; }
    .empty p { font-size: 0.95rem; }
    .refresh {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-top: 20px;
      font-size: 0.8rem;
      color: #718096;
      text-decoration: none;
      background: white;
      padding: 8px 16px;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      float: right;
    }
    .refresh:hover { color: #0088cc; }
  </style>
</head>
<body>
  <header>
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
      <circle cx="20" cy="20" r="20" fill="white" fill-opacity="0.2"/>
      <path d="M8 20l24-10-5 24-7-9-12-5z" stroke="white" stroke-width="2" stroke-linejoin="round"/>
    </svg>
    <div>
      <h1>Telegram Bot Dashboard</h1>
      <p>តាមដានអ្នកប្រើប្រាស់ Telegram Bot</p>
    </div>
  </header>

  <div class="container">
    <div class="stats">
      <div class="stat-card">
        <div class="label">អ្នកប្រើប្រាស់សរុប</div>
        <div class="value">{{ users|length }}</div>
      </div>
    </div>

    <a class="refresh" href="/">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>
      Refresh
    </a>

    <div class="card">
      <div class="card-header">អ្នកប្រើប្រាស់</div>
      {% if users %}
      <table>
        <thead>
          <tr>
            <th>User ID</th>
            <th>ឈ្មោះពេញ</th>
            <th>Username</th>
          </tr>
        </thead>
        <tbody>
          {% for user_id, info in users.items() %}
          <tr>
            <td><code>{{ user_id }}</code></td>
            <td>{{ info.full_name }}</td>
            <td>
              {% if info.username != "—" %}
                <span class="badge">@{{ info.username }}</span>
              {% else %}
                <span style="color:#a0aec0">—</span>
              {% endif %}
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
      {% else %}
      <div class="empty">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
        <p>មិនទាន់មានអ្នកប្រើប្រាស់ណាមួយទេ<br/>ផ្ញើ /start នៅ Telegram bot ដើម្បីចាប់ផ្តើម</p>
      </div>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

@app_web.route("/")
def dashboard():
    return render_template_string(HTML, users=users)

def run_bot():
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN not set — bot polling skipped.")
        return

    async def _poll():
        bot_app = ApplicationBuilder().token(TOKEN).build()
        bot_app.add_handler(CommandHandler("start", start))
        async with bot_app:
            await bot_app.start()
            await bot_app.updater.start_polling()
            await asyncio.Event().wait()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_poll())

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app_web.run(host="0.0.0.0", port=PORT, debug=False)
