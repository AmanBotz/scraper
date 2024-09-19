import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_video_and_thumbnail(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        video_urls = []
        thumbnail_urls = []

        # Debugging log for the response content
        logger.info(f"Scraping URL: {url}")

        # Find all video containers on the page
        for item in soup.find_all('div', class_='thumb-list__item video-thumb'):
            video_tag = item.find('a', href=True)
            thumbnail_tag = item.find('img', src=True)

            if video_tag and thumbnail_tag:
                video_url = video_tag['href']
                thumbnail_url = thumbnail_tag['src']

                # Filter and add URLs starting with the required patterns
                if video_url.startswith('https://xhamster.com/videos/'):
                    video_urls.append(video_url)
                if thumbnail_url.startswith('https://ic-vt-nss.xhcdn.com/a/'):
                    thumbnail_urls.append(thumbnail_url)

        # Log the result of scraping
        logger.info(f"Found {len(video_urls)} video URLs and {len(thumbnail_urls)} thumbnail URLs.")

        # Return video and thumbnail URLs
        return video_urls, thumbnail_urls

    except Exception as e:
        logger.error(f"An error occurred while scraping: {e}")
        return [], []
