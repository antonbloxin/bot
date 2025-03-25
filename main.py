import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context) -> None:
    # Отправляем приветственное сообщение
    await update.message.reply_text("🏛️ Я Гермес! Бот проекта 300 Терм. Помогу вам получить нужные материалы.")

    # Задержка 3 секунды перед отправкой меню
    await asyncio.sleep(3)

    # Определяем кнопки меню
    keyboard = [
        [InlineKeyboardButton("📄 Получить КП", callback_data='get_kp')],
        [InlineKeyboardButton("📑 Получить Техусловия", callback_data='get_tech')],
        [InlineKeyboardButton("📊 Получить Презентацию", callback_data='get_presentation')],
        [InlineKeyboardButton("🎥 Посмотреть Видео", callback_data='watch_video')],
        [InlineKeyboardButton("📂 Посмотреть кейсы", callback_data='view_cases')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contacts')]
    ]

    # Создаем разметку для меню
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем меню пользователю
    await update.message.reply_text("Выберите опцию:", reply_markup=reply_markup)

def main() -> None:
    """Start the bot."""
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # on /start command - trigger the start function
    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
