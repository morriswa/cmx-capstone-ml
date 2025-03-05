
from .site_map import get_all_sites
from .web import scrape_urls


def scrape(output_file_path):
    all_urls = get_all_sites()
    scrape_urls(all_urls, output_file_path)
