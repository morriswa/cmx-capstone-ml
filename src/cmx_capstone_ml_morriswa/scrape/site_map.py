import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_all_sites(url):
    
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_links = soup.find_all('a')
    unique_links = set() 

    for link in all_links:
        href = link.get('href')
        if href and not href.startswith(("mailto:", "tel:")):
            full_url = urljoin(url, href) 
            if "ku.edu" in full_url:  
                unique_links.add(full_url)

    for url in sorted(unique_links):  
        print(url)

    return list(unique_links)

