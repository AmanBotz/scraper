from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scraper import scrape_video_and_thumbnail

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send me a category URL to get video and thumbnail links!')

async def scrape(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = context.args[0]
    try:
        videos, thumbnails = scrape_video_and_thumbnail(url)
        if videos and thumbnails:
            response = "Video URLs:\n" + "\n".join(videos[:5]) + "\n\nThumbnail URLs:\n" + "\n".join(thumbnails[:5])
        else:
            response = "No valid video or thumbnail links found."
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token('7514151326:AAHv7qDprIuS6gkVSaYIzn6Fln2FYg4gtek').build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('scrape', scrape))
    app.run_polling()
