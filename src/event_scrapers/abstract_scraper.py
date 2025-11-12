class AbstractScraper:
    name = "abstract_scraper"
    start_urls = []

    def parse(self, response):
        event_htmls = self.get_all_events(reponse)
        for e in event_htmls:
            yield self.event_html_to_object(e)

    def get_start_date(event_html):
        """
        @param event_html: html object of a single event
        @return: datetime object of start date
        """
        raise NotImplementedError

    def get_event_name(event_html):
        """
        @param event_html: html object of a single event
        @return: string of event name/title
        """
        raise NotImplementedError

    def get_event_organizer(event_html):
        """
        @param event_html: html object of a single event
        @return: string of the name of event organizer/venue
        """
        raise NotImplementedError

    def get_event_url(event_html):
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
        raise NoteImplementedError

    def event_html_to_object(self, event_html):
        loader = ItemLoader(item=EventItem(), response=event_html)
        loader.add_value("name", self.get_event_name(event_html))
        loader.add_value("url", self.get_event_url(event_html))
        loader.add_value("organizer", self.get_event_organizer(event_html))
        loader.add_value("start_date", self.get_start_date(event_html))
