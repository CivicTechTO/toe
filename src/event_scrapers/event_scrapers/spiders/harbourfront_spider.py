import scrapy
import datetime

class HarbourfrontSpider(scrapy.Spider):
    name = "harbourfront"
    start_urls = ["https://harbourfrontcentre.com/whats-on/"]

    shared_attributes = {
        "organizer": "Harbourfront Centre",
    }

    def parse(self, response):
        event_htmls = self.get_all_events(response)
        for e in event_htmls:
            yield self.event_html_to_object(e)

#        with open(self.name + ".jsonl", "a") as file:
#            for e in event_htmls:
#        file.write(str(self.event_html_to_object(e)) + "\n")

    def get_all_events(self, response):
        return response.xpath(
            '//div[contains(@class, "wo-event")][not(contains(@class, "wo-event-copy"))]'
        )

    def event_html_to_object(self, event_html):
        date_str = event_html.xpath("*/div[1]/div[1]/text()").get().strip()
        if date_str == 'Every Day':
            date_obj = datetime.datetime.now()
        else:
            date_obj = datetime.datetime.strptime(date_str, "%a, %b %d, %Y")

        return {
            "date": date_obj,
            "name": event_html.xpath("*/div[1]/div[2]/text()").get().strip(),
            "link": event_html.xpath("a/@href").get(),
            "description": event_html.xpath("*/div[1]/div[4]/text()").get().strip(),
            **self.shared_attributes,
        }
