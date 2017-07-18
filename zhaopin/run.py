from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import argparse


if __name__ == '__main__':
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl('dajie')
    process.crawl('lagou')
    process.crawl('liepin')
    # process.crawl('zhipin')
    process.start()