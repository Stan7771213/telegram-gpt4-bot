import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

import gspread
from google.oauth2.service_account import Credentials

# 🔐 Токены
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GOOGLE_SHEET_ID = "17ln_xEzNMmeOQKtMKwf_Ll0Rt39ph9olmftLn331Et0"

# 🔧 OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# 🔄 Логирование в Google Таблицу
def log_to_sheet(username, user_id, message, response):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("gpt-logger.json", scopes=scope)

    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, username, str(user_id), message, response])

# 🤖 Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user = update.message.from_user
    user_name = user.username or user.full_name

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — полезный ассистент."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Произошла ошибка: {e}"

    try:
        log_to_sheet(user_name, user.id, user_input, reply)
    except Exception as log_error:
        print(f"Ошибка логирования: {log_error}")

    await update.message.reply_text(reply)

# ▶️ Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
