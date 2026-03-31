
import datetime
import scrapy
from open_event_feed.event_item import EventItem
from abstract_scraper import AbstractScraper


class HorseshoeTavernSpider(AbstractScraper):
    name = "horseshoe_tavern"
    start_urls = ["https://horseshoetavern.com/"]

    ORGANIZER_NAME = "Horseshoe Tavern"
    ORGANIZER_LINK = "https://horseshoetavern.com/"

    def get_all_events(self, response):
        return response.css(".schedule-event")

    def get_event_title(self, event_html):
        return event_html.css(".schedule-speaker-name::text").get()

    def get_event_url(self, event_html):
        return event_html.css("a::attr(href)").get()

    def get_start_date(self, event_html):
        date_str = event_html.css(".schedule-event-time")[0].css("::text").get()
        time_str = event_html.css(".schedule-event-time")[2].css("::text").get()

        if not date_str or not time_str:
            return None

        datetime_str = f"{date_str} {time_str}"
        # Example: "Tuesday, March 31, 2026 8:00 pm"
        # Parse into datetime
        return datetime.datetime.strptime(datetime_str, "%A, %B %d, %Y %I:%M %p")
