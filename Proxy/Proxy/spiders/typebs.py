# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Proxy.items import ProxyItem
from bs4 import BeautifulSoup
from scrapy import Request, Spider
import re


class BaseSpider(Spider):
    name = 'typebs'
    start_urls = ['http://www.xsdaili.com']

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        url = response.url + \
            bs.find(
                'div', 'table table-hover panel-default panel ips ').a['href']
        yield Request(url, callback=self.parse_ip)

    def parse_ip(self, response):
        ips = re.findall(r'(\d+\.\d+\.\d+\.\d+)[^\d]+(\d+)', response.text)
        ips = {i[0] + ':' + i[1]for i in ips}
        yield ProxyItem({'ip': list(ips)})
