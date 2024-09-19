import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from scraper import scrape_video_and_thumbnail

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start command for the bot
async def start(update: Update, context):
    await update.message.reply_text('Send me a URL to scrape videos and thumbnails.')

# Handle message with URL
async def scrape(update: Update, context):
    url = update.message.text
    logger.info(f"Received URL: {url}")

    videos, thumbnails = scrape_video_and_thumbnail(url)
    if videos and thumbnails:
        response = "Video URLs:\n" + "\n".join(videos) + "\n\nThumbnail URLs:\n" + "\n".join(thumbnails)
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("No valid video or thumbnail links found.")

def main():
    # Create the Application and set the bot token from the environment variable
    app = ApplicationBuilder().token(os.getenv("BOT_TOK")).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, scrape))

    # Run the bot using polling (no port needed for polling mode)
    logger.info("Bot started. Use polling.")
    app.run_polling()

if __name__ == '__main__':
    main()
