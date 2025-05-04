import os
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# 🔑 Токены из Render Environment
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# 📡 URL скрипта Google Apps Script
GSHEET_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbya4-4PAGcMLCU9hOmQerb834JAOo8b0E90Zui79UoFYkSu-goZbCHUaX9pS_3XU5Ud/exec"

# 🤖 OpenAI клиент
client = OpenAI(api_key=OPENAI_API_KEY)

# 📤 Функция логирования в Google Таблицу через Apps Script
def send_log_to_gsheet(username, user_id, message, response):
    try:
        payload = {
            "username": username,
            "user_id": user_id,
            "message": message,
            "response": response
        }
        requests.post(GSHEET_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"Ошибка логирования в Google Таблицу: {e}")

# ✉️ Обработка входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user = update.message.from_user
    user_name = user.username or user.full_name

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — полезный помощник."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Произошла ошибка: {e}"

    # логируем
    send_log_to_gsheet(user_name, user.id, user_input, reply)

    await update.message.reply_text(reply)

# ▶️ Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
