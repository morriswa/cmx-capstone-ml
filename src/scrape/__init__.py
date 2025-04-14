
from .site_map import get_all_ku_sites_with_depth_priority
from .web import scrape_urls


def scrape(output_file_path):
    all_urls = get_all_ku_sites_with_depth_priority("https://ku.edu/")
    scrape_urls(all_urls, output_file_path)
