# algorithm for scraping websites

# imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

# main function that takes parameter of site to be scrapped
def scrape_admissions(site_url, data):

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
    
    # site department
    site_department = soup_object.find_all(class_="site-title-group__site-title") # saves all instances of the class site-title-group__site-title, which is the blue text at the top left of every ku site
    cleaned_department = [dep.get_text().strip() for dep in site_department]

    data['Department'].append(cleaned_department[0])
    data['Page Title'].append(cleaned_titles[0])
    data['h1 Title'].append(cleaned_h1[0])
    data['Text'].append(cleaned_text)
    data['URL'].append(site_url)

    # create a pandas dataframe to store information
    example_dataframe = pd.DataFrame(data)
    print(example_dataframe)


# save all collected data in a dictionary, which will be used to make the dataframe
data_dictionary = {'Department': [],
        'Page Title': [], # I added this because H1s are not always descriptive
        'h1 Title': [],
        'Text': [],
        'URL': []
        }

# example usage on admissions.ku.edu
scrape_admissions("https://admissions.ku.edu/afford", data_dictionary)