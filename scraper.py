import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_video_and_thumbnail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    videos = []
    thumbnails = []

    # Debugging log for the response content
    logger.info(f"Scraping URL: {url}")

    # Find all video containers on the page
    for item in soup.find_all('div', class_='thumb-list__item video-thumb video-thumb--type-video'):
        # Extract the video URL
        video_url = item.find('a', class_='video-thumb__image-container')['href']
        if video_url.startswith('/videos/'):
            video_url = 'https://xhamster.com' + video_url
        if "https://xhamster.com/videos/" in video_url:
            videos.append(video_url)
        else:
            logger.warning(f"Video URL not found for item: {item}")

        # Extract the thumbnail URL
        thumbnail_tag = item.find('img', class_='tnum-1 thumb-image-container__image')
        if thumbnail_tag:
            thumbnail_url = thumbnail_tag['src']
            if thumbnail_url.startswith('https://ic-vt-nss.xhcdn.com/'):
                thumbnails.append(thumbnail_url)
            else:
                logger.warning(f"Thumbnail URL not matching expected pattern: {thumbnail_url}")
        else:
            logger.warning(f"Thumbnail tag not found for item: {item}")

    # Log the result of scraping
    logger.info(f"Found {len(video_urls)} video URLs and {len(thumbnail_urls)} thumbnail URLs.")

    return videos, thumbnails
