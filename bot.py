import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

TOKEN = os.getenv("TOKEN")  # Берём токен из переменной окружения

if not TOKEN:
    raise ValueError("Токен не найден! Убедитесь, что он указан в .env")

# Функция для отправки приветственного сообщения
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Гермес")

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
