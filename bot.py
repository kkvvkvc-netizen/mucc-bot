from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from pytube import YouTube
import os

BOT_TOKEN = "8441993377:AAFXqf6CEep0bojnZSB8mwWN-qTkBrnxh64"
OWNER_ID = 7113888398  # مالك البوت

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اهلا حبي 🌹\nدز اسم الأغنية وانا اجبلك الرابط + ملف MP3 ❤️")

async def search_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("ثواني حبي… دا ادور 🔍🎵")

    try:
        yt = YouTube(f"https://www.youtube.com/results?search_query={query}")
        title = yt.title
        url = yt.watch_url

        kb = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔗 رابط الاغنية", url=url)]]
        )

        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(filename="song.mp3")

        await update.message.reply_audio(
            audio="song.mp3",
            caption=f"🎵 {title}",
            reply_markup=kb
        )

        os.remove("song.mp3")

    except Exception:
        await update.message.reply_text("ماكدر ألكه شي، جرب كلمة ثانية 🙏")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_song))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())