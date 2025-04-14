import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def get_all_ku_sites_with_depth_priority(start_url, visited=None, depth=0, max_depth=3, all_ku_links=None):
    if visited is None:
        visited = set()
    if all_ku_links is None:
        all_ku_links = set()
    if start_url in visited or depth > max_depth:
        return all_ku_links

    visited.add(start_url)

    try:
        response = requests.get(start_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        all_links_on_page = soup.find_all('a')

        # First, extract and add all unique ku.edu links from the current page
        for link in all_links_on_page:
            href = link.get('href')
            if href and not href.startswith(("mailto:", "tel:")):
                full_url = urljoin(start_url, href)
                if "ku.edu" in full_url:
                    all_ku_links.add(full_url)

        # Then, recursively visit other ku.edu links found on this page
        for link in all_links_on_page:
            href = link.get('href')
            if href and not href.startswith(("mailto:", "tel:")):
                full_url = urljoin(start_url, href)
                if "ku.edu" in full_url and full_url not in visited:
                    get_all_ku_sites_with_depth_priority(full_url, visited, depth + 1, max_depth, all_ku_links)

        time.sleep(0.1) # To avoid overwhelming the server with requests

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {start_url}: {e}")

    return sorted(list(all_ku_links))






# #A function that gets all the sites from a given URL KR
# def get_all_sites(url):
#     #Get the response from the URL, and parse it with BeautifulSoup KR
#     response = requests.get(url, timeout=10)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     #Find all the links in the page KR
#     all_links = soup.find_all('a')
#     #Create a set to store the unique links KR
#     unique_links = set() 

#     #Iterate through all the links KR
#     for link in all_links:
#         #Get the href attribute from the link KR
#         href = link.get('href')
#         #If the href attribute is not None, and does not start with mailto: or tel: KR
#         if href and not href.startswith(("mailto:", "tel:")):
#             #Join the URL with the href attribute KR
#             full_url = urljoin(url, href) 
#             #If the URL contains "ku.edu" KR
#             if "ku.edu" in full_url:  
#                 #Add the full URL to the set KR
#                 unique_links.add(full_url)
#     #Sort the unique links and print them KR
#     for url in sorted(unique_links):  
#         print(url)
#     #Return the unique links KR
#     return list(unique_links)

