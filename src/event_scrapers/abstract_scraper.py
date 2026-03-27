from open_event_feed.event_item import EventItem

class AbstractScraper:
    name = ""
    start_urls = []

    def parse(self, response):
        event_htmls = self.get_all_events(response)
        for e in event_htmls:
            yield self.event_html_to_object(e)

    def get_start_date(self, event_html):
        """
        @param event_html: html object of a single event
        @return: datetime object of start date
        """
        raise NotImplementedError

    def get_event_title(self, event_html):
        """
        @param event_html: html object of a single event
        @return: string of event name/title
        """
        raise NotImplementedError

    def get_event_organizer(self, event_html):
        """
        @param event_html: html object of a single event
        @return: string of the name of event organizer/venue
        """
        raise NotImplementedError

    def get_event_url(self, event_html):
        """
        @param event_html: html object of a single event
        @return: string of the event url. Unique per event
        """
        raise NotImplementedError

    def get_all_events(self, response):
        """
        @param reponse: scrapy response object
        @return: array of html selectors
        """
        raise NotImplementedError

    def event_html_to_object(self, event_html):
        return EventItem(
            title=self.get_event_title(event_html),
            link=self.get_event_url(event_html),
            organizer_link=self.ORGANIZER_LINK,
            organizer_name=self.ORGANIZER_NAME,
            start_datetime=self.get_start_date(event_html)
        )

