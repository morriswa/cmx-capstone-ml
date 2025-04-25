
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

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

def is_allowed_url(url):
    return not any(domain in url for domain in DISALLOWED_DOMAINS)

def safe_get(url, retries=3, backoff_factor=1.5):
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            wait = backoff_factor * (2 ** i)
            print(f"[Retry {i + 1}] Waiting {wait:.1f}s for {url} due to error: {e}")
            time.sleep(wait)
    print(f"[Failed] Could not fetch: {url}")
    return None

def get_all_sites_with_depth_priority(start_url, visited=None, depth=0, max_depth=3, all_links=None):
    if visited is None:
        visited = set()
    if all_links is None:
        all_links = set()
    if start_url in visited or depth > max_depth:
        return all_links

    visited.add(start_url)

    response = safe_get(start_url)
    if response is None:
        return all_links

    soup = BeautifulSoup(response.text, 'html.parser')
    all_links_on_page = soup.find_all('a')

    for link in all_links_on_page:
        href = link.get('href')
        if href and not href.startswith(("mailto:", "tel:", "javascript:")):
            full_url = urljoin(start_url, href)
            if is_allowed_url(full_url):
                all_links.add(full_url)

    for link in all_links_on_page:
        href = link.get('href')
        if href and not href.startswith(("mailto:", "tel:")):
            full_url = urljoin(start_url, href)
            if is_allowed_url(full_url) and full_url not in visited:
                get_all_sites_with_depth_priority(full_url, visited, depth + 1, max_depth, all_links)

    time.sleep(0.5)  # Slight delay between pages to reduce load

    return list(all_links)

