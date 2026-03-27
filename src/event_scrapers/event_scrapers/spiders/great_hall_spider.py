import datetime
import scrapy
from scrapy.loader import ItemLoader
from open_event_feed.event_item import EventItem

class PhoenixSpider(scrapy.Spider):
    name = "great_hall"
    start_urls = ["https://thegreathall.ca/calendar/"]

    def parse(self, response):
        event_htmls = self.get_all_events(response)
        for e in event_htmls:
            yield self.event_html_to_object(e)

    def get_all_events(self, response):
        return response.css(".tgh-event-item-container")

    def event_html_to_object(self, event_html):
        return EventItem(
            title=event_html.css(".tgh-e-title::text").get(),
            link=event_html.css("a").attrib["href"],
            organizer_link="https://thegreathall.ca/",
            organizer_name="The Great Hall",
            start_datetime=self.get_start_date(event_html)
        )

    def get_start_date(self, event_html):
        print(event_html)
        # Extract text
        date_str = event_html.css(".tgh-e-date::text").get()
        time_str = event_html.css(".tgh-e-time::text").get()


        if not date_str or not time_str:
            return None

        # Combine into one string
        datetime_str = f"{date_str} {time_str}"
        # Example: "Fri Mar 27 2026 10:00 pm"

        print(datetime_str)
        # Parse into datetime
        return datetime.datetime.strptime(datetime_str, "%a %b %d %Y %I:%M %p")

