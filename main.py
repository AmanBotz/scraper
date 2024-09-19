import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from scraper import scrape_videos_and_thumbnails

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Command to start the bot
async def start(update: Update, context):
    await update.message.reply_text("Send me a page URL, and I'll fetch the video and thumbnail links.")

# Handling the URL sent by the user
async def handle_url(update: Update, context):
    url = update.message.text
    try:
        video_urls, thumbnail_urls = scrape_videos_and_thumbnails(url)
        response = "Video URLs:\n" + "\n".join(video_urls[:5]) + "\n\nThumbnail URLs:\n" + "\n".join(thumbnail_urls[:5])
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await update.message.reply_text("Failed to fetch data. Please check the URL or try again later.")

# Error handler
async def error_handler(update: object, context: object):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

if __name__ == '__main__':
    # Replace 'your-bot-token' with the actual token from @BotFather
    application = Application.builder().token('your-bot-token').build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    
    # Error handler
    application.add_error_handler(error_handler)

    # Run the bot
    application.run_polling()
