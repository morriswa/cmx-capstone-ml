import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_all_sites(url):
    
    # Fetch the page
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract and clean up links
    all_links = soup.find_all('a')
    unique_links = set()  # To store unique links

    for link in all_links:
        href = link.get('href')
        if href and not href.startswith(("mailto:", "tel:")):  # Filter only 'ku.edu' links
            full_url = urljoin(url, href)  # Convert to absolute URL
            if "ku.edu" in full_url:  # Ensure it contains "ku.edu" anywhere
                unique_links.add(full_url)

    # Print cleaned-up list
    for url in sorted(unique_links):  # Sorted for readability
        print(url)

    return list(unique_links)

