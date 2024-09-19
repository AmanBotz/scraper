import requests
from bs4 import BeautifulSoup

def scrape_videos_and_thumbnails(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load page")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Modify this section based on the actual page structure
    video_elements = soup.select("a.video-thumb__image-container")  # Adjust as per the page structure
    video_urls = []
    thumbnail_urls = []
    
    for video in video_elements:
        video_url = video.get('href')
        thumbnail_url = video.find('img')['src']

        # Avoid duplicates or invalid links
        if "xhamster.com" in video_url and video_url not in video_urls:
            video_urls.append(video_url)
        if "xhamster.com" in thumbnail_url and thumbnail_url not in thumbnail_urls:
            thumbnail_urls.append(thumbnail_url)
    
    if not video_urls or not thumbnail_urls:
        raise Exception("No valid video or thumbnail links found")
    
    return video_urls, thumbnail_urls
