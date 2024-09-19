import requests
from bs4 import BeautifulSoup

def scrape_video_and_thumbnail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    videos = []
    thumbnails = []

    # Iterate over each video container
    for item in soup.find_all('div', class_='thumb-list__item video-thumb video-thumb--type-video'):
        # Extract the video URL
        video_url = item.find('a', class_='video-thumb__image-container role-pop thumb-image-container')['href']
        if video_url.startswith('/videos/'):
            video_url = 'https://xhamster.com' + video_url
        if "https://xhamster.com/videos/" in video_url:
            videos.append(video_url)

        # Extract the thumbnail URL
        thumbnail_tag = item.find('img', class_='tnum-1 thumb-image-container__image')
        if thumbnail_tag:
            thumbnail_url = thumbnail_tag['src']
            if "https://ic-vt-nss.xhcdn.com/" in thumbnail_url:
                thumbnails.append(thumbnail_url)

    return videos, thumbnails
