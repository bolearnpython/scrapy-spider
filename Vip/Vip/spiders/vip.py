# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Vip.items import VipItem
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, SelectJmes


class VipSpider(Spider):
    name = 'vip'
    allowed_domains = ['vip.com']

    def start_requests(self):
        url = 'https://detail.vip.com/detail-1907957-330569011.html'
        yield Request(url)

    def parse(self, response):
        loader = ItemLoader(item=VipItem(), response=response)
        loader.add_css('price', 'div.pi-price-box em::text')
        loader.add_css('zhekou', 'div.pi-price-box span.pbox-off::text')
        loader.add_css('oprice', 'div.pi-price-box del.J-mPrice::text')
        loader.add_css('title', 'div.pib-title p::text')
        loader.add_css('imgs', 'div.pic-sliderwrap a::attr(href)')
        yield loader.load_item()
