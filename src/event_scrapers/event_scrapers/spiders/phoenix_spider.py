import datetime
import scrapy
from open_event_feed.event_item import EventItem
from abstract_scraper import AbstractScraper


class PhoenixSpider(AbstractScraper):
    name = "phoenix"
    start_urls = ["https://thephoenixconcerttheatre.com/events/page/1"]

    ORGANIZER_NAME = "The Phoenix Concert Theatre"
    ORGANIZER_LINK = "https://thephoenixconcerttheatre.com/"

    def get_all_events(self, response):
        return response.css(".event-item")

    def get_event_title(self, event_html):
        return event_html.css("span.sr-only::text").get()

    def get_event_url(self, event_html):
        return event_html.css("a::attr(href)").get()

    def get_event_organizer(self, event_html):
        # Static in this case
        return self.ORGANIZER_NAME

    def get_start_date(self, event_html):
        """
        Example input: "Friday, Oct 17, Doors: 7pm"
        """
        now = datetime.datetime.now()
        year = now.year

        date_str = event_html.css("header.event-date::text").get()
        if not date_str:
            return None

        date_str = date_str.strip()

        parts = date_str.split(", ")
        if len(parts) < 3:
            return None

        month_day = parts[1].strip()
        time_part = parts[2].split("Doors:")[-1].strip()

        full_str = f"{month_day} {year} {time_part}"

        try:
            dt = datetime.datetime.strptime(full_str, "%b %d %Y %I:%M%p")
        except ValueError:
            dt = datetime.datetime.strptime(full_str, "%b %d %Y %I%p")

        # Handle year rollover
        if dt < now:
            dt = dt.replace(year=year + 1)

        return dt
