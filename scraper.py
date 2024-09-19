import requests
from bs4 import BeautifulSoup

def scrape_video_and_thumbnail(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    video_links = []
    thumbnail_links = []

    # Find all video items in the page
    for item in soup.find_all('div', class_='thumb-list__item video-thumb video-thumb--type-video'):
        video_url = item.find('a', class_='video-thumb__image-container')['href']
        if 'https://xhamster.com/videos/' in video_url and not any(ext in video_url for ext in ['.mp4', '.avi', '.mov']):
            video_links.append(video_url)
        
        thumbnail_url = item.find('img', class_='tnum-1 thumb-image-container__image')['src']
        if 'https://ic-vt-nss.xhcdn.com/' in thumbnail_url:
            thumbnail_links.append(thumbnail_url)

    # Remove duplicates
    video_links = list(set(video_links))
    thumbnail_links = list(set(thumbnail_links))

    return video_links, thumbnail_links

# Test the function
url = 'https://xhamster.com/categories/indian'  # replace with the actual URL
videos, thumbnails = scrape_video_and_thumbnail(url)

print("Video URLs:")
for video in videos[:5]:  # Displaying the first 5 links
    print(video)

print("\nThumbnail URLs:")
for thumbnail in thumbnails[:5]:  # Displaying the first 5 links
    print(thumbnail)
