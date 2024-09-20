import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to check if the video is available based on the "Video is not available" div
def is_video_playable(video_url):
    try:
        # Fetch the video page to check if the "Video is not available" message exists
        response = requests.get(video_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check for the "Video is not available" message
        unavailable_message = soup.find('div', class_='noindexed-text', attrs={'data-text': 'Video is not available'})
        if unavailable_message:
            logger.warning(f"Video is not available: {video_url}")
            return False
        return True
    except Exception as e:
        logger.error(f"Error checking video availability for {video_url}: {e}")
        return False

def scrape_video_and_thumbnail(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        soup = BeautifulSoup(response.content, 'html.parser')

        videos = []
        thumbnails = []

        logger.info(f"Scraping URL: {url}")

        # Iterate over each video container
        for idx, item in enumerate(soup.find_all('div', class_='thumb-list__item video-thumb video-thumb--type-video')):
            logger.info(f"Processing item #{idx + 1}")

            # Extract the video URL
            video_tag = item.find('a', class_='video-thumb__image-container')
            if video_tag:
                video_url = video_tag['href']
                if video_url.startswith('/videos/'):
                    video_url = 'https://xhamster.com' + video_url
                if "https://xhamster.com/videos/" in video_url:
                    # Check if the video is available (playable)
                    if is_video_playable(video_url):
                        videos.append(video_url)
                        logger.info(f"Found playable video URL: {video_url}")

                        # Extract the corresponding thumbnail URL since the video is playable
                        thumbnail_tag = item.find('img', class_='thumb-image-container__image')
                        if thumbnail_tag:
                            thumbnail_url = thumbnail_tag['src']
                            if thumbnail_url.startswith('https://ic-vt-nss.xhcdn.com/'):
                                thumbnails.append(thumbnail_url)
                                logger.info(f"Found thumbnail URL: {thumbnail_url}")
                            else:
                                logger.warning(f"Invalid thumbnail URL pattern: {thumbnail_url}")
                        else:
                            logger.warning(f"No thumbnail tag found for item #{idx + 1}")
                    else:
                        logger.warning(f"Skipping unavailable video URL: {video_url}")
                else:
                    logger.warning(f"Invalid video URL pattern: {video_url}")
            else:
                logger.warning(f"No video URL found for item #{idx + 1}")

        # Log results
        logger.info(f"Scraping completed. Found {len(videos)} playable video URLs and {len(thumbnails)} corresponding thumbnail URLs.")

        return videos, thumbnails

    except Exception as e:
        logger.error(f"An error occurred while scraping: {e}")
        return [], []
        
