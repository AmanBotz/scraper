import requests
from bs4 import BeautifulSoup

def scrape_video_and_thumbnail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    videos = []
    thumbnails = []

    # Extract videos and thumbnails from the page
    for item in soup.find_all('div', class_="thumb-list__item video-thumb video-thumb--type-video"):
        # Safely extract video URL
        video_link = item.find('a', class_='video-thumb__image-container')
        if video_link and 'href' in video_link.attrs:
            video_url = video_link['href']
            if video_url.startswith('https://xhamster.com/videos/'):
                videos.append(video_url)
        else:
            continue  # Skip if no valid video link is found

        # Safely extract thumbnail URL
        thumbnail_img = item.find('img', class_='tnum-1 thumb-image-container__image')
        if thumbnail_img and 'src' in thumbnail_img.attrs:
            thumbnail_url = thumbnail_img['src']
            if thumbnail_url.startswith('https://ic-vt-nss.xhcdn.com/'):
                thumbnails.append(thumbnail_url)

    return videos, thumbnails
