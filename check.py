import requests
from bs4 import BeautifulSoup
import logging
from scraper import scrape_video_and_thumbnail

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example: Proxy settings for a free Indian proxy
proxies = {
    'http': 'http://103.170.62.7:8080',
    'https': 'http://160.25.180.35:8080'
}

# Function to check if a video is available based on the "Video is not available" message
def is_video_playable(video_url):
    try:
        logger.info(f"Checking video availability for: {video_url} via Indian proxy")
        # Add a timeout (e.g., 10 seconds) to avoid long waits for unresponsive proxies
        response = requests.get(video_url, proxies=proxies, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check if the "Video is not available" message exists
        unavailable_message = soup.find('div', class_='noindexed-text', attrs={'data-text': 'Video is not available'})
        if unavailable_message:
            logger.info(f"Video is not available: {video_url}")
            return False

        logger.info(f"Video is available: {video_url}")
        return True

    except requests.exceptions.Timeout:
        logger.error(f"Timeout occurred while checking video availability for {video_url}")
        return False  # Treat as unavailable if the proxy is too slow

    except requests.exceptions.ProxyError:
        logger.error(f"Proxy error while checking video availability for {video_url}")
        return False  # Treat as unavailable if the proxy fails

    except Exception as e:
        logger.error(f"Error checking video availability for {video_url}: {e}")
        return False

# Function to check each video and filter unavailable ones
def check_and_generate_files(url):
    videos, thumbnails = scrape_video_and_thumbnail(url)

    available_videos = []
    available_thumbnails = []

    for idx, video_url in enumerate(videos):
        if is_video_playable(video_url):
            available_videos.append(video_url)
            available_thumbnails.append(thumbnails[idx])

    # Write video URLs to a text file
    video_file_path = "/tmp/video_urls.txt"
    with open(video_file_path, "w") as video_file:
        for video in available_videos:
            video_file.write(f"{video}\n")

    # Write thumbnail URLs to a text file
    thumbnail_file_path = "/tmp/thumbnail_urls.txt"
    with open(thumbnail_file_path, "w") as thumb_file:
        for thumbnail in available_thumbnails:
            thumb_file.write(f"{thumbnail}\n")

    logger.info(f"Available videos: {len(available_videos)}, Available thumbnails: {len(available_thumbnails)}")
    return video_file_path, thumbnail_file_path
