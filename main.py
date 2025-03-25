import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

bot = Bot(token="7622349875:AAFCIO5bZ0qddUQnBVMCuysXMbuAGXLLVTs")

# Функция для отправки приветствия и меню с задержкой
async def start(update: Update, context):
    await update.message.reply_text("🏛️ Я Гермес! Бот проекта 300 Терм. Помогу вам получить нужные материалы.")

    # Задержка 3 секунды перед отправкой меню
    await asyncio.sleep(3)

    keyboard = [
        ["📄 Получить КП", "📑 Получить Техусловия"],
        ["📊 Получить Презентацию", "🎥 Посмотреть Видео"],
        ["📂 Посмотреть кейсы", "📞 Контакты"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("👇 Выберите интересующий раздел:", reply_markup=reply_markup)

# Функция обработки кнопок
async def handle_message(update: Update, context):
    text = update.message.text

    if text == "📄 Получить КП":
        try:
            with open("kp.pdf", "rb") as doc:
                await update.message.reply_document(doc, caption="📄 Вот актуальное КП.")
        except FileNotFoundError:
            await update.message.reply_text("❌ Ошибка: файл КП не найден!")

    elif text == "📑 Получить Техусловия":
        try:
            with open("tech_usloviya.pdf", "rb") as doc:
                await update.message.reply_document(doc, caption="📑 Вот технические условия.")
        except FileNotFoundError:
            await update.message.reply_text("❌ Ошибка: файл техусловий не найден!")

    elif text == "📊 Получить Презентацию":
        try:
            with open("presentation.pdf", "rb") as doc:
                await update.message.reply_document(doc, caption="📊 Вот презентация проекта.")
        except FileNotFoundError:
            await update.message.reply_text("❌ Ошибка: файл презентации не найден!")

    elif text == "🎥 Посмотреть Видео":
        await update.message.reply_text(
            "🎥 Видео о проекте: [Посмотреть на YouTube](https://www.youtube.com/)", 
            parse_mode="Markdown"
        )

    elif text == "📂 Посмотреть кейсы":
        try:
            with open("cases.pdf", "rb") as doc:
                await update.message.reply_document(doc, caption="📂 Вот кейсы проекта.")
        except FileNotFoundError:
            await update.message.reply_text("❌ Ошибка: файл кейсов не найден!")

    elif text == "📞 Контакты":
        await update.message.reply_text(
            "📧 Email: info@300term.ru\n📞 Телефон: +7 (999) 123-45-67\n🌐 Сайт: [300 Терм](https://300term.ru)",
            parse_mode="Markdown"
        )

    else:
        await update.message.reply_text("Я не понял команду. Выберите пункт меню! 👇")

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
