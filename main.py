import os
import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from check import check_and_generate_files
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

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

    # Call the check_and_generate_files function to get valid video and thumbnail URLs
    video_file, thumbnail_file = check_and_generate_files(url)

    if video_file and thumbnail_file:
        # Send the video URLs file
        with open(video_file, "rb") as vf:
            await update.message.reply_document(InputFile(vf, filename="video_urls.txt"))

        # Send the thumbnail URLs file
        with open(thumbnail_file, "rb") as tf:
            await update.message.reply_document(InputFile(tf, filename="thumbnail_urls.txt"))

        # Clean up files after sending
        os.remove(video_file)
        os.remove(thumbnail_file)
    else:
        await update.message.reply_text("No valid video or thumbnail links found.")

# Function to start a simple HTTP server for health checks
def run_http_server():
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8000))), handler)
    logger.info("HTTP server started for health check")
    httpd.serve_forever()

def main():
    # Start HTTP server in a separate thread for health checks
    thread = threading.Thread(target=run_http_server)
    thread.daemon = True
    thread.start()

    # Create the Application and set the bot token from the environment variable
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, scrape))

    # Run the bot using polling
    logger.info("Bot started. Use polling.")
    app.run_polling()

if __name__ == '__main__':
    main()
