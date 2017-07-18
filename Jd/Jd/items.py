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
    price = scrapy.Field()
    title = scrapy.Field()
    param = scrapy.Field()
    comment_hot = scrapy.Field()
    comment_pro = scrapy.Field()


class Jd_Com_Item(scrapy.Item):
    _id = scrapy.Field()
    ID = scrapy.Field()
    content = scrapy.Field()
    creationTime = scrapy.Field()
    images = scrapy.Field()
    nickname = scrapy.Field()
    productColor = scrapy.Field()
    productSales = scrapy.Field()
    productSize = scrapy.Field()
    referenceName = scrapy.Field()
    referenceTime = scrapy.Field()
    score = scrapy.Field()
    userClientShow = scrapy.Field()
    userLevelName = scrapy.Field()
