import argparse

def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

src = "./abstract_scraper.py"
parser = argparse.ArgumentParser(
                    prog='NewScraper',
                    description='Creates a new scraper'
)
parser.add_argument('scraper_name')
args = parser.parse_args()

scraper_name = args.scraper_name 

scraper_code = f"""
import datetime
import scrapy
from open_event_feed.event_item import EventItem
from abstract_scraper import AbstractScraper


class {to_camel_case(scraper_name)}Spider(AbstractScraper):
    name = "{scraper_name}"
    start_urls = []

    ORGANIZER_NAME = ""
    ORGANIZER_LINK = ""

    def get_all_events(self, response):
        return response.css(".event-item")

    def get_event_title(self, event_html):
        return event_html.css("span.sr-only::text").get()

    def get_event_url(self, event_html):
        return event_html.css("a::attr(href)").get()

    def get_start_date(self, event_html):
        return dt
"""

with open(f"./event_scrapers/spiders/{scraper_name}_spider.py", "w") as f:
    f.write(scraper_code)