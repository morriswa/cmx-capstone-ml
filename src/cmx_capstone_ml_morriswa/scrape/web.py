# algorithm for scraping websites

# imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

# function that scrapes all the urls from a list of sites KR
def scrape_urls(all_urls, csv_filename) -> None:
    # dictionary to store all the data
    data_dictionary = {'Department': [],
        'Page Title': [], # I added this because H1s are not always descriptive
        'h1 Title': [],
        'Text': [],
        'URL': []
        }
    for site in all_urls:
        scrape_function(site, data_dictionary)

    # create a pandas dataframe to store information
    dataframe = pd.DataFrame(data_dictionary)
    print(dataframe)

    dataframe.to_csv(csv_filename)
    

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