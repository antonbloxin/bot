import logging
import os
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Обработчик нажатия кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка нажатий на кнопки."""
    query = update.callback_query
    await query.answer()  # Подтверждаем нажатие кнопки
    
    if query.data == "watch_video":
        # Отправляем сообщение с описанием и ссылкой
        await query.message.reply_text(
            "ГК Новые термы занимается комплексно разработкой и реализацией высокодоходных инвестиционных проектов в сфере термальных комплексов по всей России.\n\n"
            "Наша цель - это создание экосистемы, состоящей из 300 термальных комплексов и IT-инфраструктуры через создание сбалансированной и взаимовыгодной системы отношений инвесторов, команды и гостей.\n\n"
            "Эта работа не ограничивается лишь цифрами и проектами; она заключается в создании ценности для общества, улучшении качества жизни людей и формировании новой структуры отдыха.\n\n"
            "Подробнее о наших проектах, целях и кейсах смотрите в презентации генерального директора Александра Рудакова.\n\n"
            "Ссылка на видео: https://rutube.ru/video/3ac6026b1823bc07e3159736102caae1/"
        )

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    # Приветственное сообщение
    await update.message.reply_text("🏛️ Я Гермес! Бот проекта 300 Терм. Помогу вам получить нужные материалы.")
    
    # Задержка 3 секунды перед отправкой меню
    await asyncio.sleep(3)

    # Определение кнопок для меню
    keyboard = [
        [InlineKeyboardButton("📄 Получить КП", callback_data='get_kp')],
        [InlineKeyboardButton("📑 Получить Техусловия", callback_data='get_tech')],
        [InlineKeyboardButton("📊 Получить Презентацию", callback_data='get_presentation')],
        [InlineKeyboardButton("🎥 Посмотреть Видео", callback_data='watch_video')],
        [InlineKeyboardButton("📂 Посмотреть кейсы", callback_data='view_cases')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contacts')]
    ]

    # Создание разметки с кнопками
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем меню
    await update.message.reply_text("Выберите опцию:", reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(
        os.environ.get("TOKEN")
    ).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Обработка нажатий кнопок
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
