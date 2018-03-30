# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Dianying.items import DianyingItem
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, SelectJmes
import re


def strip_x(value):
    if isinstance(value, str):
        if '◎' in value:
            return value.replace('\u3000', '', 2).replace('\u3000', ':')
        value = re.sub('\s', '', value)
        if len(value) > 0:
            return value
        else:
            return


class Ygdy8Spider(Spider):
    name = 'ygdy8'
    allowed_domains = ['ygdy8.com']
    host_url = 'http://www.ygdy8.com'

    def start_requests(self):
        url = 'http://www.ygdy8.com/html/gndy/dyzz/index.html'
        yield Request(url)

    def parse(self, response):
        for url in response.css('b a::attr(href)').extract():
            url = self.host_url + url
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        loader = ItemLoader(item=DianyingItem(), response=response)
        next_loader = loader.nested_css('div#Zoom')
        next_loader.add_xpath('info', '*//text()',
                              MapCompose(strip_x))
        yield loader.load_item()
