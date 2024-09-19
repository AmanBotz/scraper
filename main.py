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

        # Call the scraper function
        videos, thumbnails = scrape_video_and_thumbnail(url)

        if videos and thumbnails:
            # Check if URLs are scraped properly
            logger.info(f"Scraped {len(videos)} video URLs and {len(thumbnails)} thumbnail URLs")

            # Write video URLs to a text file with the correct .txt extension
            video_file_path = "video_urls.txt"
            with open(video_file_path, "w") as video_file:
                for video in videos:
                    video_file.write(f"{video}\n")

            # Write thumbnail URLs to a text file with the correct .txt extension
            thumbnail_file_path = "thumbnail_urls.txt"
            with open(thumbnail_file_path, "w") as thumb_file:
                for thumbnail in thumbnails:
                    thumb_file.write(f"{thumbnail}\n")

            # Send the video URLs file
            await update.message.reply_document(InputFile(video_file_path))

            # Send the thumbnail URLs file
            await update.message.reply_document(InputFile(thumbnail_file_path))

            # Optionally, clean up the files after sending
            os.remove(video_file_path)
            os.remove(thumbnail_file_path)
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
