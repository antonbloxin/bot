import os
from telegram import Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

TOKEN = os.getenv("TOKEN")  # Берём токен из переменной окружения

# Функция для отправки приветственного сообщения
async def start(update: Update, context):
    await update.message.reply_text("Привет")

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()