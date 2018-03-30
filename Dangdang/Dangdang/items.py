# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader.processors import Join, MapCompose, TakeFirst


class DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # id = scrapy.Field() #过滤
    href = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    search_shangjia = scrapy.Field()
    search_shangjia_link = scrapy.Field()
    star = scrapy.Field()
    comment = scrapy.Field()
    search_book_author = scrapy.Field()
