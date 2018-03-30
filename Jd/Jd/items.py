# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # id = scrapy.Field() #过滤
    _id = scrapy.Field()
    hot = scrapy.Field()
    comments = scrapy.Field()
    product = scrapy.Field()


class Item_Detail(scrapy.Item):
    # define the fields for your item here like:
    # id = scrapy.Field() #过滤
    _id = scrapy.Field()
    price = scrapy.Field()
