import datetime
import scrapy
from scrapy.loader import ItemLoader
from event_item import EventItem


class PhoenixSpider(scrapy.Spider):
    name = "phoenix"
    start_urls = ["https://thephoenixconcerttheatre.com/events/page/1"]

    def parse(self, response):
        event_htmls = self.get_all_events(response)
        for e in event_htmls:
            yield self.event_html_to_object(e)

    def get_all_events(self, response):
        return response.css(".event-item")

    def event_html_to_object(self, event_html):
        loader = ItemLoader(item=EventItem(), response=event_html)
        loader.add_value(
            "start_date", self.get_start_date(event_html)
        )
        loader.add_value("name", event_html.css("span.sr-only::text").get())
        loader.add_value("organizer", "Phoenix Theatre")
        loader.add_value("url", event_html.css("a").attrib["href"])
        return loader.load_item()

    def get_start_date(self, event_html):
        # Example input: "Friday, Oct 17, Doors: 7pm"
        now = datetime.datetime.now()
        year = now.year

        date_str = event_html.css("header.event-date::text").get().strip()

        parts = date_str.split(", ")
        month_day = parts[1].strip()
        time_part = parts[2].split("Doors:")[-1].strip()

        full_str = f"{month_day} {year} {time_part}"

        # Try parsing time with and without minutes
        try:
            dt = datetime.datetime.strptime(full_str, "%b %d %Y %I:%M%p")
        except ValueError:
            dt = datetime.datetime.strptime(full_str, "%b %d %Y %I%p")

        # Phoenix does not include the year in the object, but we know they only
        #  post events for the future, so we can account for events happening next year
        if dt < now:
            dt = dt.replace(year=year+1)

        return dt