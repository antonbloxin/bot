import logging
import os
import asyncio
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# FILE_ID моего стикера
STICKER_ID = "CAACAgIAAxkBAAEN0kVn5DosnEUsvrIq3qMijI-UH06IRwAChXkAAtiRIEslui9KsGyRWzYE"

# Файл для хранения статистики
STATS_FILE = "bot_stats.json"

# Мой Telegram ID 
ADMIN_ID = 1059405288 

# Функция обновления статистики
def update_stats(user_id, username, action):
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, "r", encoding="utf-8") as file:
                stats = json.load(file)
        else:
            stats = {}

        if str(user_id) not in stats:
            stats[str(user_id)] = {"username": username, "total_interactions": 0, "actions": {}}

        stats[str(user_id)]["total_interactions"] += 1
        stats[str(user_id)]["actions"][action] = stats[str(user_id)]["actions"].get(action, 0) + 1

        with open(STATS_FILE, "w", encoding="utf-8") as file:
            json.dump(stats, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка обновления статистики: {e}")

# Команда /stats (только для администратора) - отправляет DOC-файл
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
    
    doc_content = f"📊 Общая статистика:\n👤 Пользователей: {total_users}\n📈 Всего взаимодействий: {total_interactions}\n\n"
    username_list = "Список пользователей:\n"
    
    for user_id, data in stats.items():
        username = data["username"] if data["username"] else "(Нет никнейма)"
        doc_content += f"👤 @{username} (ID: {user_id})\n🔄 Всего действий: {data['total_interactions']}\n"
        username_list += f"@{username}\n"
        for action, count in data["actions"].items():
            doc_content += f"   🔹 {action}: {count}\n"
        doc_content += "\n"
    
    doc_content += "\n" + username_list
    
    stats_file_path = "bot_statistics.doc"
    with open(stats_file_path, "w", encoding="utf-8") as doc_file:
        doc_file.write(doc_content)
    
    await update.message.reply_document(open(stats_file_path, "rb"), filename="bot_statistics.doc", caption="📊 Полная статистика бота")
    os.remove(stats_file_path)

# Обработчик нажатия кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    username = query.from_user.username or "(Нет никнейма)"
    action = query.data
    
    await query.answer()
    update_stats(user_id, username, action)

    if action == "watch_video":
        await query.message.reply_text(
            "ГК Новые термы занимается комплексно разработкой и реализацией высокодоходных инвестиционных проектов..."
            "\nСсылка на видео: https://rutube.ru/video/3ac6026b1823bc07e3159736102caae1/"
        )
    elif action == "get_presentation":
        pdf_path = "Present_300term.pdf"
        await query.message.reply_text("⏳ Одну секунду... Загружаю")
        await query.message.reply_document(open(pdf_path, "rb"), caption="Презентация 300 Терм")
    elif action == "get_kp":
        kp_path = "KP_Termokomplektov.pdf"
        await query.message.reply_text("⏳ Одну секунду... Загружаю")
        await query.message.reply_document(open(kp_path, "rb"), caption="Коммерческое предложение ТермоКомплектов")
    elif action == "get_tech":
        tech_path = "Tekhnicheskiye_usloviya.pdf"
        await query.message.reply_text("⏳ Одну секунду... Загружаю")
        await query.message.reply_document(open(tech_path, "rb"), caption="Технические условия")
    elif action == "contacts":
        await query.message.reply_text("📞 Контакты:\n📧 Почта: delo@300term.ru\n📱 Телефон: +7 910-640 65 30")

def main() -> None:
    application = Application.builder().token(
        os.environ.get("TOKEN")
    ).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
