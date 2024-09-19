import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scraper import scrape_video_and_thumbnail

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send me a URL to scrape video and thumbnail links.')

async def scrape(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    try:
        videos, thumbnails = scrape_video_and_thumbnail(url)
        response = "Video URLs:\n" + "\n".join(videos) + "\n\nThumbnail URLs:\n" + "\n".join(thumbnails)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main() -> None:
    application = ApplicationBuilder().token('YOUR_TELEGRAM_BOT_TOKEN').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("scrape", scrape))

    application.run_polling()

if __name__ == '__main__':
    main()
