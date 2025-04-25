
#from .site_map import get_all_links
from .web import scrape_urls
from.site_map import get_all_sites_with_depth_priority


def scrape(output_file_path):
    #all_urls = get_all_links("https://ku.edu/")
    all_urls = get_all_sites_with_depth_priority("https://ku.edu/")
    print(f"debug: {all_urls}")
    scrape_urls(all_urls, output_file_path)
