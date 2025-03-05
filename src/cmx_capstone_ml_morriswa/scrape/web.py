# algorithm for scraping websites

# imports
import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_urls(all_urls, output_file_path) -> None:
    pass

# main function that takes parameter of site to be scrapped
def scrape_function(site_url, dictionary):

    # use requests library to get HTML contents of the site
    html_object = requests.get(site_url)
    html_content = html_object.content

    # create a BeautifulSoup object which is used to parse through the html
    soup_object = BeautifulSoup(html_content, "html5lib")

    # strip the html of <tags>
    for script_or_style in soup_object(['script', 'style']):
        script_or_style.decompose()  # removes the tag

    # variable that contains all of the site's text
    cleaned_text = soup_object.get_text(separator=' ', strip=True)

    # h1s
    headings = soup_object.find_all('h1') # saves all h1s to a list
    cleaned_h1 = [heading.get_text().strip() for heading in headings]

    # site titles
    site_titles = soup_object.find_all('title') # saves all title tags to a list (the name that appears on a browser tab)
    cleaned_titles = [title.get_text().strip() for title in site_titles]
    first_title = cleaned_titles[0]
    first_part = first_title.split(" | ")[0]
    
    # site department
    site_department = soup_object.find_all(class_="site-title-group__site-title") # saves all instances of the class site-title-group__site-title, which is the blue text at the top left of every ku site
    cleaned_department = [dep.get_text().strip() for dep in site_department]

    dictionary['Department'].append(cleaned_department[0])
    dictionary['Page Title'].append(first_part)
    dictionary['h1 Title'].append(cleaned_h1[0])
    dictionary['Text'].append(cleaned_text)
    dictionary['URL'].append(site_url)

# # save all collected data in a dictionary, which will be used to make the dataframe
# data_dictionary = {'Department': [],
#         'Page Title': [], # I added this because H1s are not always descriptive
#         'h1 Title': [],
#         'Text': [],
#         'URL': []
#         }

# # example of a list of sites to scrape
# example_list = ["https://accessibility.ku.edu",
# "https://affordability.ku.edu/costs",
# "https://canvas.ku.edu",
# "https://cms.ku.edu",
# "https://directory.ku.edu/",
# "https://employment.ku.edu/",
# "https://financialaid.ku.edu/consumer-information",
# "https://humanresources.ku.edu/",
# "https://iss.ku.edu/",
# "https://ku.edu",
# "https://kupolice.ku.edu/",
# "https://lib.ku.edu/",
# "https://my.ku.edu",
# "https://my.ku.edu/JayhawkGpsRedirect",
# "https://news.ku.edu/",
# "https://opsmaps.ku.edu/",
# "https://otp.ku.edu/",
# "https://policy.ku.edu/provost/privacy-policy",
# "https://publicaffairs.ku.edu/freedom-of-expression",
# "https://registrar.ku.edu/",
# "https://registrar.ku.edu/ku-academic-calendar",
# "https://registrar.ku.edu/transcripts",
# "https://sa.ku.edu",
# "https://technology.ku.edu/"]
#
# for site in example_list:
#     scrape_function(site, data_dictionary)
#
# # create a pandas dataframe to store information
# example_dataframe = pd.DataFrame(data_dictionary)
# print(example_dataframe)
