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

# Команда /broadcast - отправка сообщений всем пользователям (только для администратора)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет доступа к этой команде.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Используйте: /broadcast [ваше сообщение]")
        return

    message_text = " ".join(context.args)
    
    if not os.path.exists(STATS_FILE):
        await update.message.reply_text("Нет пользователей для рассылки.")
        return

    with open(STATS_FILE, "r", encoding="utf-8") as file:
        stats = json.load(file)

    sent_count = 0
    for user_id in stats.keys():
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message_text)
            sent_count += 1
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение {user_id}: {e}")
    
    await update.message.reply_text(f"✅ Сообщение отправлено {sent_count} пользователям.")
    
# Команда /delete - удаление сообщений
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет доступа к этой команде.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Используйте: /delete [message_id]")
        return

    message_id = context.args[0]
    
    if not os.path.exists(MESSAGES_FILE):
        await update.message.reply_text("Нет сообщений для удаления.")
        return

    with open(MESSAGES_FILE, "r", encoding="utf-8") as file:
        messages = json.load(file)

    deleted_count = 0
    for user_id, message_ids in messages.items():
        if message_id in message_ids:
            try:
                await context.bot.delete_message(chat_id=int(user_id), message_id=int(message_id))
                message_ids.remove(message_id)
                deleted_count += 1
            except Exception as e:
                logger.error(f"Не удалось удалить сообщение {message_id} у {user_id}: {e}")
    
    with open(MESSAGES_FILE, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)

    await update.message.reply_text(f"✅ Сообщение {message_id} удалено у {deleted_count} пользователей.")

# Команда /messageid - получение списка отправленных сообщений
async def messageid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет доступа к этой команде.")
        return

    if not os.path.exists(MESSAGES_FILE):
        await update.message.reply_text("Нет сохранённых сообщений.")
        return

    with open(MESSAGES_FILE, "r", encoding="utf-8") as file:
        messages = json.load(file)

    message_text = "📨 Список отправленных сообщений:\n"
    for user, msg_ids in messages.items():
        message_text += f"👤 Пользователь {user}: {', '.join(map(str, msg_ids))}\n"
    
    await update.message.reply_text(message_text)


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

# Команда /stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет доступа к этой команде.")
        return

    if not os.path.exists(STATS_FILE):
        await update.message.reply_text("Статистика пока не собиралась.")
        return

    with open(STATS_FILE, "r", encoding="utf-8") as file:
        stats = json.load(file)
    
    total_users = len(stats)
    total_interactions = sum(user["total_interactions"] for user in stats.values())
    
    message = f"📊 Общая статистика:\n👤 Пользователей: {total_users}\n📈 Всего взаимодействий: {total_interactions}\n\n"
    
    for user_id, data in stats.items():
        username = data["username"] if data["username"] else "(Нет никнейма)"
        message += f"👤 @{username} (ID: {user_id})\n🔄 Всего действий: {data['total_interactions']}\n"
        for action, count in data["actions"].items():
            message += f"   🔹 {action}: {count}\n"
        message += "\n"
    
    await update.message.reply_text(message)

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

