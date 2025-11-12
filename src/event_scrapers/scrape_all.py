import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

def run_all_spiders():
    settings = get_project_settings()

    configure_logging()

    process = CrawlerProcess(settings)

    for spider_name in process.spider_loader.list():
        process.crawl(spider_name)

    process.start()

if __name__ == "__main__":
    run_all_spiders()

