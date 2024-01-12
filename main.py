from scraper import scrape_page
from store import add_codes
from webhook import notify_discord


def main():
    code_details = scrape_page()
    add_codes(code_details)
    notify_discord(code_details)


main()
