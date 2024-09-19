import os
import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters
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
        # Write video URLs to a text file
        video_file_path = "/tmp/video_urls.txt"
        with open(video_file_path, "w") as video_file:
            video_file.write("\n".join(videos))

        # Write thumbnail URLs to a text file
        thumbnail_file_path = "/tmp/thumbnail_urls.txt"
        with open(thumbnail_file_path, "w") as thumb_file:
            thumb_file.write("\n".join(thumbnails))

        # Send the video URLs file
        await update.message.reply_document(InputFile(video_file_path, filename="video_urls.txt"))

        # Send the thumbnail URLs file
        await update.message.reply_document(InputFile(thumbnail_file_path, filename="thumbnail_urls.txt"))

        # Optionally, clean up the files after sending
        os.remove(video_file_path)
        os.remove(thumbnail_file_path)
    else:
        await update.message.reply_text("No valid video or thumbnail links found.")

def main():
    # Create the Application and set the bot token from the environment variable
    app = ApplicationBuilder().token(os.getenv("BOT_TOK")).build()

    # Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, scrape))

    # Run the bot using polling
    logger.info("Bot started. Use polling.")
    app.run_polling()

if __name__ == '__main__':
    main()
