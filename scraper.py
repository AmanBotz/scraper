import requests
from bs4 import BeautifulSoup

def scrape_video_and_thumbnail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    videos = []
    thumbnails = []

    # Extract videos and thumbnails from the page
    for item in soup.find_all('div', class_="thumb-list__item video-thumb video-thumb--type-video"):
        video_url = item.find('a', class_='video-thumb__image-container')['href']
        if video_url.startswith('https://xhamster.com/videos/'):
            videos.append(video_url)

        thumbnail_url = item.find('img', class_='tnum-1 thumb-image-container__image')['src']
        if thumbnail_url.startswith('https://ic-vt-nss.xhcdn.com/'):
            thumbnails.append(thumbnail_url)

    return videos, thumbnails
