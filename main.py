import logging
import os
import asyncio
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# FILE_ID твоего стикера (замени на актуальный)
STICKER_ID = "CAACAgIAAxkBAAEN0kVn5DosnEUsvrIq3qMijI-UH06IRwAChXkAAtiRIEslui9KsGyRWzYE"

# Файл для хранения статистики
STATS_FILE = "bot_stats.json"
# Файл для хранения отправленных сообщений
MESSAGES_FILE = "sent_messages.json"

# Твой Telegram ID (замени на свой)
ADMIN_ID = 1059405288  # Укажи свой Telegram ID

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "(Нет никнейма)"
    update_stats(user_id, username, "start")

    await update.message.reply_sticker(STICKER_ID)
    await asyncio.sleep(1)
    await update.message.reply_text("🏛️ Я Гермес! Бот проекта 300 Терм. Помогу вам получить нужные материалы.")
    await asyncio.sleep(2)
    keyboard = [
        [InlineKeyboardButton("📄 Получить КП", callback_data='get_kp')],
        [InlineKeyboardButton("📑 Получить Техусловия", callback_data='get_tech')],
        [InlineKeyboardButton("📊 Получить Презентацию", callback_data='get_presentation')],
        [InlineKeyboardButton("🎥 Посмотреть Видео", callback_data='watch_video')],
        [InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/termsnew")],
        [InlineKeyboardButton("📞 Контакты", callback_data='contacts')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите опцию:", reply_markup=reply_markup)

# Обработчик нажатия кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    username = query.from_user.username or "(Нет никнейма)"
    action = query.data
    
    await query.answer()
    update_stats(user_id, username, action)
    
    if action == "get_kp":
        await query.message.reply_text("⏳ Одну секунду... Загружаю")
        await query.message.reply_document(open("KP_Termokomplektov.pdf", "rb"), caption="Коммерческое предложение ТермоКомплектов")
    elif action == "get_tech":
        await query.message.reply_text("⏳ Одну секунду... Загружаю")
        await query.message.reply_document(open("Tekhnicheskiye_usloviya.pdf", "rb"), caption="Технические условия")
    elif action == "get_presentation":
        await query.message.reply_text("⏳ Одну секунду... Загружаю")
        await query.message.reply_document(open("Present_300term.pdf", "rb"), caption="Презентация 300 Терм")
    elif action == "watch_video":
        await query.message.reply_text("ГК Новые термы занимается комплексно разработкой и реализацией высокодоходных инвестиционных проектов...\nСсылка на видео: https://rutube.ru/video/3ac6026b1823bc07e3159736102caae1/")
    elif action == "contacts":
        await query.message.reply_text("📞 Контакты:\n📧 Почта: delo@300term.ru\n📱 Телефон: +7 910-640 65 30")

def main() -> None:
    application = Application.builder().token(
        os.environ.get("TOKEN")
    ).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("messageid", messageid))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
