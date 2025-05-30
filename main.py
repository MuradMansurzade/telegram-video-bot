import os
import re
from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# 🔑 Вставь сюда токен своего бота от @BotFather
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅ Проверка, является ли сообщение поддерживаемой ссылкой
def is_supported_link(text: str) -> bool:
    patterns = [
        r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/",
        r"(https?://)?(www\.)?tiktok\.com/",
        r"(https?://)?(www\.)?instagram\.com/"
    ]
    return any(re.search(p, text) for p in patterns)

# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Пришли мне ссылку на TikTok, YouTube или Instagram — я скачаю тебе видео без водяных знаков!")

# 💬 Обработка сообщений с ссылкой
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not is_supported_link(url):
        await update.message.reply_text("⚠ Поддерживаются только ссылки на TikTok, YouTube и Instagram.")
        return

    await update.message.reply_text("⏳ Скачиваю видео...")

    try:
        # Опции для yt_dlp
        ydl_opts = {
            'outtmpl': 'downloads/%(title).80s.%(ext)s',
            'format': 'mp4',
            'quiet': True,
            'no_warnings': True,
        }

        # Создать папку downloads
        os.makedirs("downloads", exist_ok=True)

        # Скачать видео
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Отправить видео пользователю
        with open(filename, 'rb') as video_file:
            await update.message.reply_video(video=video_file)

        # Удалить файл после отправки
        os.remove(filename)

    except Exception as e:
        print("Ошибка:", e)
        await update.message.reply_text("❌ Произошла ошибка при скачивании видео.")

# ▶ Основная функция
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

# 🔁 Запуск
if __name__ == "__main__":
    main()