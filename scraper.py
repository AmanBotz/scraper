import requests
from bs4 import BeautifulSoup

def scrape_video_and_thumbnail(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    soup = BeautifulSoup(response.text, 'html.parser')

    videos = []
    thumbnails = []

    for item in soup.find_all("div", class_="thumb-list__item video-thumb video-thumb--type-video"):
        video_url = item.find('a', class_='video-thumb__image-container')['href']
        thumbnail_url = item.find('img', class_='tnum-1 thumb-image-container__image')['src']

        if video_url.startswith("https://xhamster.com/videos/") and thumbnail_url.startswith("https://ic-vt-nss.xhcdn.com/a/"):
            videos.append(video_url)
            thumbnails.append(thumbnail_url)

    if not videos or not thumbnails:
        raise ValueError("No valid video or thumbnail links found")

    return videos, thumbnails
