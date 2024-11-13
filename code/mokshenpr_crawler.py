import requests
from bs4 import BeautifulSoup
import time

# getting all links from the start URL
def get_all_links(start_url):
    links = set()
    response = requests.get(start_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href = True):
            url = link['href']
            if url.startswith('/'):
                url = start_url + url
                
            if url.startswith('http'):
                links.add(url)
                
    return links

def download_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeuatifulSoup(response.text, 'html.parser')
        return soup.get_text(separator = '\n', strip = True)
    return ""

start_url = 'https://mokshapr.ru'

page_urls = get_all_links(start_url)

for i, url in enumerate(page_urls):
    page_text = download_text(url)

    filename = f"page_text_{i}.txt"
    with open(filename, "w", encoding = "utf-8") as file:
        file.write(page_text)

        time.sleep(1)
