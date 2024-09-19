import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext

from scraper import scrape_video_and_thumbnail

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Handle incoming messages
async def handle_message(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.text:
            url = update.message.text
            logger.info(f"Received URL: {url}")

            videos, thumbnails = scrape_video_and_thumbnail(url)

            if videos and thumbnails:
                response = "Video URLs:\n" + "\n".join(videos) + "\n\nThumbnail URLs:\n" + "\n".join(thumbnails)

                # Split the message if it's too long
                for i in range(0, len(response), 4096):  # Telegram's message size limit is 4096 characters
                    await update.message.reply_text(response[i:i+4096])
            else:
                await update.message.reply_text("No videos or thumbnails found.")
        else:
            logger.error("No message text found in update.")
            await update.message.reply_text("Please send a valid URL.")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Main function to start the bot
if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOK")
    app = ApplicationBuilder().token(TOKEN).build()

    # Add a message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started. Use polling.")
    app.run_polling()
