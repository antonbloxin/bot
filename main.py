import logging
import os
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Обработчик нажатия кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "watch_video":
        await query.message.reply_text(
            "ГК Новые термы занимается комплексно разработкой и реализацией высокодоходных инвестиционных проектов..."
            "\nСсылка на видео: https://rutube.ru/video/3ac6026b1823bc07e3159736102caae1/"
        )
    
    elif query.data == "get_presentation":
        pdf_path = "Present_300term.pdf"
        await query.message.reply_document(open(pdf_path, "rb"), caption="Презентация 300 Терм")
    
    elif query.data == "get_kp":
        kp_path = "KP_Termokomplektov.pdf"
        await query.message.reply_document(open(kp_path, "rb"), caption="Коммерческое предложение Термокомплектов")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🏛️ Я Гермес! Бот проекта 300 Терм. Помогу вам получить нужные материалы.")
    await asyncio.sleep(2)
    keyboard = [
        [InlineKeyboardButton("📄 Получить КП", callback_data='get_kp')],
        [InlineKeyboardButton("📑 Получить Техусловия", callback_data='get_tech')],
        [InlineKeyboardButton("📊 Получить Презентацию", callback_data='get_presentation')],
        [InlineKeyboardButton("🎥 Посмотреть Видео", callback_data='watch_video')],
        [InlineKeyboardButton("📂 Посмотреть кейсы", callback_data='view_cases')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contacts')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите опцию:", reply_markup=reply_markup)

def main() -> None:
    application = Application.builder().token(
        os.environ.get("TOKEN")
    ).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
