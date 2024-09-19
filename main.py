import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from scraper import scrape_video_and_thumbnail

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start command
async def start(update: Update, context):
    await update.message.reply_text("Send me a URL and I'll fetch the videos and thumbnails.")

# Handle URLs
async def handle_message(update: Update, context):
    url = update.message.text
    logger.info(f"Received URL: {url}")
    
    try:
        videos, thumbnails = scrape_video_and_thumbnail(url)
        if videos and thumbnails:
            response = "Video URLs:\n" + "\n".join(videos) + "\n\nThumbnail URLs:\n" + "\n".join(thumbnails)
        else:
            response = "No valid video or thumbnail links found."
        
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await update.message.reply_text(f"An error occurred: {e}")

def main():
    # Create the Application and pass your bot's token.
    app = Application.builder().token(os.getenv("BOT_TOK")).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    logger.info("Bot started. Use polling.")
    app.run_polling()

if __name__ == "__main__":
    main()
