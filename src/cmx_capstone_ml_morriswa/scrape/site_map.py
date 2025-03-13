import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#A function that gets all the sites from a given URL KR
def get_all_sites(url):
    #Get the response from the URL, and parse it with BeautifulSoup KR
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Find all the links in the page KR
    all_links = soup.find_all('a')
    #Create a set to store the unique links KR
    unique_links = set() 

    #Iterate through all the links KR
    for link in all_links:
        #Get the href attribute from the link KR
        href = link.get('href')
        #If the href attribute is not None, and does not start with mailto: or tel: KR
        if href and not href.startswith(("mailto:", "tel:")):
            #Join the URL with the href attribute KR
            full_url = urljoin(url, href) 
            #If the URL contains "ku.edu" KR
            if "ku.edu" in full_url:  
                #Add the full URL to the set KR
                unique_links.add(full_url)
    #Sort the unique links and print them KR
    for url in sorted(unique_links):  
        print(url)
    #Return the unique links KR
    return list(unique_links)

