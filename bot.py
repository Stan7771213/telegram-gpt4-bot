{\rtf1\ansi\ansicpg1251\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import openai\
from telegram import Update\
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters\
\
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")\
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")\
\
openai.api_key = OPENAI_API_KEY\
\
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):\
    user_input = update.message.text\
    try:\
        response = openai.ChatCompletion.create(\
            model="gpt-4",\
            messages=[\
                \{"role": "system", "content": "\uc0\u1058 \u1099  \'97 \u1087 \u1086 \u1083 \u1077 \u1079 \u1085 \u1099 \u1081  \u1087 \u1086 \u1084 \u1086 \u1097 \u1085 \u1080 \u1082 ."\},\
                \{"role": "user", "content": user_input\}\
            ]\
        )\
        reply = response.choices[0].message.content.strip()\
    except Exception as e:\
        reply = f"\uc0\u1055 \u1088 \u1086 \u1080 \u1079 \u1086 \u1096 \u1083 \u1072  \u1086 \u1096 \u1080 \u1073 \u1082 \u1072 : \{e\}"\
\
    await update.message.reply_text(reply)\
\
def main():\
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()\
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))\
    app.run_polling()\
\
if __name__ == "__main__":\
    main()\
}