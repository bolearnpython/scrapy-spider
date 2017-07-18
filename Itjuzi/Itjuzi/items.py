# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    # define the fields for your item here like:
    # id = scrapy.Field() #过滤
    title = scrapy.Field()
    slogan = scrapy.Field()
    local = scrapy.Field()
    scope = scrapy.Field()
    link = scrapy.Field()
    tags = scrapy.Field()
    des = scrapy.Field()
    des_more = scrapy.Field()
    nb = scrapy.Field()
    indus_info = scrapy.Field()
    text_info = scrapy.Field()
    company_number_in = scrapy.Field()
    company_number_out = scrapy.Field()
    product_info = scrapy.Field()
    invst_info = scrapy.Field()
