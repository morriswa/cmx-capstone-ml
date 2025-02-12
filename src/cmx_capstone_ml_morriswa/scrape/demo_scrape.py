# algorithm for scraping websites

# imports
import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_admissions():
    # url of website that will be scraped
    URL = "https://admissions.ku.edu"

    html_object = requests.get(URL)
    html_content = html_object.content

    # create BeautifulSoup object used to parse through and find things in html
    soup_object = BeautifulSoup(html_content, "html5lib")
    # print(soup_object.prettify()) # this prints the html formatted correctly

    # code to find all h1s and h2s and add them to a list
    headings = soup_object.find_all('h1')
    heading2s = soup_object.find_all('h2')

    # create a pandas dataframe to store information (this doesn't work yet)
    example_dataframe = pd.DataFrame(columns=['Department', 'Title', 'HTML', 'URL'])
