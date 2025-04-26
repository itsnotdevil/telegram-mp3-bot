import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv('7532011979:AAGk4o7BkdactJz6WoEuXUFpk-uBM1T0F6s')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎶 Send me a YouTube URL and I'll send you the MP3!")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    try:
        await update.message.reply_text("⏳ Downloading audio...")

        filename = "audio.mp3"
        command = [
            "yt-dlp",
            "-x", "--audio-format", "mp3",
            "-o", filename,
            url
        ]
        subprocess.run(command, check=True)

        await update.message.reply_audio(audio=open(filename, 'rb'))

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))

    app.run_polling()

if __name__ == '__main__':
    main()
