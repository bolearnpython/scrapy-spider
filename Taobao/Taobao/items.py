# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # id = scrapy.Field() #过滤
    shop = scrapy.Field()
    shop_link = scrapy.Field()
    shop_rate = scrapy.Field()
    shop_sellor = scrapy.Field()
    info = scrapy.Field()
    imgs = scrapy.Field()
    title = scrapy.Field()
    infos = scrapy.Field()
