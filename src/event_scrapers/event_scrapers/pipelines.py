# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class EventScrapersPipeline:
    def process_item(self, item, spider):
        with open("./scraped_data/" + spider.name + ".jsonl", "a") as file:
            # TODO: write sqlite writer
            adapter = ItemAdapter(item)            
            d = adapter.asdict()
            file.write(str(d) + "\n")

        return item
