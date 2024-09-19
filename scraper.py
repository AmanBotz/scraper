import requests
from bs4 import BeautifulSoup

def scrape_video_and_thumbnail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    videos = []
    thumbnails = []

    for item in soup.find_all('div', class_='thumb-list__item'):
        video_link = item.find('a', class_='video-thumb__image-container')['href']
        thumbnail_link = item.find('img', class_='tnum-1 thumb-image-container__image')['src']
        
        if 'https://xhamster.com/videos/' in video_link and not any(video_link.endswith(ext) for ext in ['.mp4', '.avi', '.mov']):
            videos.append(video_link)
            thumbnails.append(thumbnail_link)

    return list(set(videos)), list(set(thumbnails))  # Remove duplicates

