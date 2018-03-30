# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VipItem(scrapy.Item):
    # define the fields for your item here like:
    # id = scrapy.Field() #过滤
    price = scrapy.Field()
    zhekou = scrapy.Field()
    oprice = scrapy.Field()
    title = scrapy.Field()
    imgs = scrapy.Field()
