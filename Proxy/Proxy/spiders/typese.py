# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Proxy.items import ProxyItem
from bs4 import BeautifulSoup
from scrapy import Request, Spider
import re
import ipdb


class BaseSpider(Spider):
    '''端口  js   变化'''

    name = 'typese'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'Proxy.middlewares.JSMiddleware': 200, }
    }
    url1 = ['http://www.goubanjia.com/free/gngn/index%s.shtml' %
            i for i in range(1, 30)]
    url2 = []
    start_urls = url1 + url2

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, meta={'PhantomJS': True})

    def parse(self, response):
        if response.url in self.url2:
            ips = re.findall(
                r'(\d+\.\d+\.\d+\.\d+)[^\d]+100.*?(\d+)', response.text)
            yield ProxyItem({'ip': list(ips)})
        else:
            bs = BeautifulSoup(response.text, 'lxml')
            ips = [[i.text for i in ip(['span', 'div'])]
                   for ip in bs.find('tbody')('td', 'ip')]
            [x.insert(-1, ":") for x in ips]
            ips = [''.join(ip) for ip in ips]
            yield ProxyItem({'ip': list(ips)})
