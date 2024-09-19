import requests
from bs4 import BeautifulSoup

def scrape_video_and_thumbnail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    video_urls = []
    thumbnail_urls = []

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

    # Return video and thumbnail URLs
    return video_urls, thumbnail_urls
