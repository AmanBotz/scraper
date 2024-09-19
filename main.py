import os
import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
from scraper import scrape_video_and_thumbnail

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: CallbackContext):
    try:
        url = update.message.text
        logger.info(f"Received URL: {url}")

        videos, thumbnails = scrape_video_and_thumbnail(url)

        if videos and thumbnails:
            # Write video URLs to a text file
            with open("video_urls.txt", "w") as video_file:
                video_file.write("\n".join(videos))

            # Write thumbnail URLs to a text file
            with open("thumbnail_urls.txt", "w") as thumb_file:
                thumb_file.write("\n".join(thumbnails))

            # Send the video URLs file
            await update.message.reply_document(InputFile("video_urls.txt"))

            # Send the thumbnail URLs file
            await update.message.reply_document(InputFile("thumbnail_urls.txt"))

            # Optionally, clean up the files after sending
            os.remove("video_urls.txt")
            os.remove("thumbnail_urls.txt")
        else:
            await update.message.reply_text("No valid video or thumbnail links found.")
    
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await update.message.reply_text(f"An error occurred: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("BOT_TOK")).build()

    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started. Use polling.")
    app.run_polling()
