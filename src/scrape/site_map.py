"""
site_map.py

This script is designed to scrape websites. 
It avoids scraping domains listed in the DISALLOWED_DOMAINS list to respect privacy 
and legal boundaries. The script includes functionality to:

1. Check if a URL is allowed based on the disallowed domains list.
2. Safely retrieve web pages with retry and exponential backoff mechanisms.
3. Recursively collect all links from a starting URL up to a specified depth, 
   while ensuring that disallowed domains are excluded.

Dependencies:
- requests: For making HTTP requests.
- BeautifulSoup (from bs4): For parsing HTML content.
- urllib.parse: For handling URL joining.
"""


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

#List of domains we want to avoid scraping for privacy and ethical reasons
DISALLOWED_DOMAINS = [
    "twitter.com", "facebook.com", "instagram.com", "youtube.com",
    "linkedin.com", "tiktok.com", "snapchat.com", "pinterest.com",
    "theatlantic.com", "theguardian.com", "nytimes.com", "washingtonpost.com",
    "bbc.com", "cnn.com", "forbes.com", "businessinsider.com",
    "huffpost.com", "buzzfeed.com", "reddit.com", "quora.com",
    "wikipedia.org", "wikihow.com", "fandom.com", "wikia.com",
    "tumblr.com", "blogger.com", "wordpress.com", "medium.com",
    "blogspot.com", "livejournal.com", "typepad.com", "weebly.com",
    "usnews.com", "govtrack.us", "congress.gov", "govinfo.gov",
    "nasa.gov", "noaa.gov", "cdc.gov", "epa.gov",
    "fda.gov", "nih.gov", "usda.gov", "usgs.gov",  
    "loc.gov", "archives.gov", "whitehouse.gov", "justice.gov",
    "state.gov", "defense.gov", "treasury.gov", "commerce.gov",
    "labor.gov", "education.gov", "transportation.gov", "energy.gov",
    "interior.gov", "hud.gov", "va.gov", "dhs.gov",
    "sba.gov", "nrc.gov", "fcc.gov", "ftc.gov",
    "sec.gov", "cftc.gov", "fdic.gov", "federalreserve.gov", "studentaid.gov",
    "irs.gov", "ssa.gov", "cms.gov", "dol.gov",
    "sba.gov","hhs.gov"
]

def is_allowed_url(url): #Checks to see if the website is in the disallowed domains
    return not any(domain in url for domain in DISALLOWED_DOMAINS)

# Attempt to safely retrieve a URL with retry and exponential backoff
def safe_get(url, retries=3, backoff_factor=1.5):
    for i in range(retries): # Retry up to 'retries' times
        try: 
            response = requests.get(url, timeout=10) # Set a timeout for the request
            response.raise_for_status() # Raise an error for bad responses
            return response # Return the response if successful
        except requests.exceptions.RequestException as e: # Handle any request exceptions
            wait = backoff_factor * (2 ** i) # Exponential backoff
            print(f"[Retry {i + 1}] Waiting {wait:.1f}s for {url} due to error: {e}") # Log the error
            time.sleep(wait) # Wait before retrying
    print(f"[Failed] Could not fetch: {url}") # Log the failure
    return None

# Function to get all sites with depth priority
def get_all_sites_with_depth_priority(start_url, visited=None, depth=0, max_depth=3, all_links=None):
    if visited is None: # Initialize visited set if not provided
        visited = set() # Initialize visited set
    if all_links is None: # Initialize all_links set if not provided
        all_links = set() # Initialize all_links set
    if start_url in visited or depth > max_depth: # Check if URL is already visited or max depth is reached
        return all_links # Return if already visited or max depth reached

    visited.add(start_url) # Add the current URL to visited set

    response = safe_get(start_url) # Attempt to safely get the URL
    if response is None: # If the response is None, return all_links
        return all_links #Return if the response is None

    soup = BeautifulSoup(response.text, 'html.parser') # Parse the HTML content
    all_links_on_page = soup.find_all('a') # Find all links on the page

    for link in all_links_on_page: # Iterate through all links on the page
        href = link.get('href') # Get the href attribute
        if href and not href.startswith(("mailto:", "tel:", "javascript:")): # Ignore mailto, tel, and javascript links
            full_url = urljoin(start_url, href) # Create the full URL
            if is_allowed_url(full_url): # Check if the URL is allowed
                all_links.add(full_url) # Add the URL to all_links set

    for link in all_links_on_page: # Iterate through all links on the page again for depth priority
        href = link.get('href') # Get the href attribute
        if href and not href.startswith(("mailto:", "tel:")): # Ignore mailto and tel links
            full_url = urljoin(start_url, href) # Create the full URL
            if is_allowed_url(full_url) and full_url not in visited: # Check if the URL is allowed and not visited
                get_all_sites_with_depth_priority(full_url, visited, depth + 1, max_depth, all_links) # Recursively call the function for depth priority

    time.sleep(0.5)  # Slight delay between pages to reduce load

    return list(all_links) # Return all links as a list

