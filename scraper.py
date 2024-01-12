import requests
from bs4 import BeautifulSoup
import csv
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())

uri = os.environ.get('MONGO_URI')
webhook_url = os.environ.get('WEBHOOK_URL')

client = MongoClient(uri)

dbs = client.list_database_names()
codes_db = client.codes

code_details = []
collection = codes_db.codes


def scrape_page(soup, code_details):
    code_elements = soup.find_all('table')

    code_rows = code_elements[0].find('tbody').find_all("tr")
    for code_row in code_rows:
        code_tds = code_row.find_all("td")

        details = []
        for code_td in code_tds:
            details.append(code_td.text)

        code = details[0]
        gift = details[1]
        expire_date = details[2]

        existing_code = collection.find_one({"gift": gift})
        if not existing_code:
            code_details.append(
                {
                    'code': code,
                    'gift': gift,
                    'expire_date': expire_date
                }
            )


def add_codes(codes):
    if len(code_details) != 0:
        collection.insert_many(codes)
        webhook = DiscordWebhook(url=webhook_url)
        embed = DiscordEmbed(title="New codes", description="Go to site", color="03b2f8")
        webhook.add_embed(embed)
        response = webhook.execute()
    else:
        print("No new codes")


# def get_codes(code_details):
#     for code in code_details:
#         exist = collection.find_one({'gift': code['gift']})
#         # print(exist)
#         if exist is not None:
#             codes_keeper.append(exist)


# the url of the home page of the target website
base_url = 'https://www.nintendolife.com/guides/pokemon-scarlet-and-violet-mystery-gift-codes-list'

# defining the User-Agent header to use in the GET request below
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64;'
                  ' x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

page = requests.get(base_url, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')

scrape_page(soup, code_details)
# get_codes(code_details)
add_codes(code_details)

csv_file = open('codes.csv', 'w', encoding='utf-8', newline='')

writer = csv.writer(csv_file)

writer.writerow(['Code', 'Gift', 'Expire Date'])

for code_detail in code_details:
    writer.writerow(code_detail.values())

csv_file.close()
