# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    floor = scrapy.Field()
    name = scrapy.Field()
    zone = scrapy.Field()
    price_one_metter = scrapy.Field()
    cx = scrapy.Field()
    title = scrapy.Field()
    img = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    jjr = scrapy.Field()
    metter = scrapy.Field()
    link = scrapy.Field()
    price_one_month = scrapy.Field()
    tags = scrapy.Field()
    build_time = scrapy.Field()
    _type = scrapy.Field()
    bus = scrapy.Field()
    zu_type = scrapy.Field()
    update_time = scrapy.Field()
    detail = scrapy.Field()
    follow = scrapy.Field()
