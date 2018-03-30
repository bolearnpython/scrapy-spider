from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
if __name__ == '__main__':
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    for spider_name in process.spiders.list():
        process.crawl(spider_name)
    process.start()
