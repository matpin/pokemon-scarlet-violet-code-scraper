import requests
from bs4 import BeautifulSoup


def scrape_page(soup, code_details):
    code_elements = soup.find_all('table')


# the url of the home page of the target website
base_url = 'https://www.nintendolife.com/guides/pokemon-scarlet-and-violet-mystery-gift-codes-list'

# defining the User-Agent header to use in the GET request below
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64;'
                  ' x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

page = requests.get(base_url, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')

code_details = []

scrape_page(soup, code_details)
