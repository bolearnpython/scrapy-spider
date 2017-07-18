# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Tmall.items import TmallItem
from bs4 import BeautifulSoup
from scrapy import Request, Spider
import re


class TmallSpider(Spider):
    name = 'tmall'
    allowed_domains = ['tmall.com']

    def start_requests(self):
        url = 'https://detail.tmall.com/item.htm?id=526571132217&skuId=3134614899606&user_id=682444557&cat_id=53306006&is_b=1&rn=3a35ee5dd44ebad6e036a7353e3d6c17'
        yield Request(url, dont_filter=True)

    def parse(self, response):
        print(response.url)
        print(response.url)
        yield Request('https://detail.m.tmall.com/item.htm?id=531841713885')
