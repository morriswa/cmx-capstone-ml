# algorithm for scraping websites

# imports
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse

SKIP_DOMAINS = [
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
def is_valid_http_url(url):
    try: 
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https')  
    except Exception as e:
        print(f"Error parsing URL '{url}': {e}")
        return False

# function that scrapes all the urls from a list of sites KR
def scrape_urls(all_urls, csv_filename) -> None:

    # dictionary to store all the data
    data_dictionary = {'Department': [],
        'Page Title': [], # I added this because H1s are not always descriptive
        'h1 Title': [],
        'Text': [],
        'URL': []
        }
    
    valid_urls = []

    for site in all_urls:
        if any(domain in site for domain in SKIP_DOMAINS):
            print(f"[SKIPPED] Skipping government site: {site}")
            continue
        if not is_valid_http_url(site):
            print(f"Invalid URL: {site}")
            continue
        try:
            
            scrape_function(site, data_dictionary)
            valid_urls.append(site)
        except Exception as e:
            print(f"Skipped invalid URL: {site} due to error: {e}")
            continue

    # create a pandas dataframe to store information
    dataframe = pd.DataFrame(data_dictionary)
    print(dataframe)

    dataframe.to_csv(csv_filename)

    # Print the list of valid URLs at the end
    print("Successfully scraped the following URLs:")
    for url in valid_urls:
        print(url)


# main function that takes parameter of site to be scrapped
def scrape_function(site_url, dictionary):

    try:
        # use requests library to get HTML contents of the site
        html_object = requests.get(site_url)
    
        # check if the response is HTML before parsing
        content_type = html_object.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            print(f"[SKIPPED] Non-HTML content at: {site_url} (Content-Type: {content_type})")
            return
        html_content = html_object.content
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch {site_url}: {e}")
        return

    # create a BeautifulSoup object which is used to parse through the html
    soup_object = BeautifulSoup(html_content, "html5lib")

    # strip the html of <tags>
    for script_or_style in soup_object(['script', 'style']):
        script_or_style.decompose()  # removes the tag

    # variable that contains all of the site's text
    cleaned_text = soup_object.get_text(separator=' ', strip=True)

    # h1s
    headings = soup_object.find_all('h1') # saves all h1s to a list

    # handle cases where site has no h1
    if headings == []:
        cleaned_h1 = ["N/A"]
    else:
        cleaned_h1 = [heading.get_text().strip() for heading in headings]

    # site titles
    site_titles = soup_object.find_all('title') # saves all title tags to a list (the name that appears on a browser tab)
    
    # handle cases where site has no title tags
    if site_titles == []:
        first_title_cleaned = "N/A"
    else:
        cleaned_titles = [title.get_text().strip() for title in site_titles]
        first_title = cleaned_titles[0]
        first_title_cleaned = first_title.split(" | ")[0]

    # site department
    site_department = soup_object.find_all(class_="site-title-group__site-title") # saves all instances of the class site-title-group__site-title, which is the blue text at the top left of every ku site
    
    # handle cases where site has no site-title-group__site-title tag
    if site_department == []:
        department_cleaned = ["N/A"]
    else:
        department_cleaned = [dep.get_text().strip() for dep in site_department][0] # return first element in cleaned departments list

    # add scraped data into a dictionary
    dictionary['Department'].append(department_cleaned)
    dictionary['Page Title'].append(first_title_cleaned)
    dictionary['h1 Title'].append(cleaned_h1[0])
    dictionary['Text'].append(cleaned_text)
    dictionary['URL'].append(site_url)




#### testing ####
# example of a list of sites to scrape for testing 
#example_list = ["https://accessibility.ku.edu",
#"https://affordability.ku.edu/costs",
#"https://canvas.ku.edu",
#"https://cms.ku.edu",
#"https://directory.ku.edu/",
#"https://employment.ku.edu/",
#"https://financialaid.ku.edu/consumer-information",
#"https://humanresources.ku.edu/",
#"https://iss.ku.edu/",
#"https://ku.edu",
#"https://kupolice.ku.edu/",
#"https://lib.ku.edu/",
#"https://my.ku.edu",
#"https://my.ku.edu/JayhawkGpsRedirect",
#"https://news.ku.edu/",
#"https://opsmaps.ku.edu/",
#"https://otp.ku.edu/",
#"https://policy.ku.edu/provost/privacy-policy",
#"https://publicaffairs.ku.edu/freedom-of-expression",
#"https://registrar.ku.edu/",
#"https://registrar.ku.edu/ku-academic-calendar",
#"https://registrar.ku.edu/transcripts",
#"https://sa.ku.edu",
#"https://technology.ku.edu/"]

#scrape_urls(example_list, 'ku_csv')