 # -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ToutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    href = scrapy.Field()
    title = scrapy.Field()
    labels = scrapy.Field()
    content = scrapy.Field()
    is_article = scrapy.Field()
    articleInfo = scrapy.Field()