# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    zu = scrapy.Field()
    uid = scrapy.Field()
    user = scrapy.Field()
    base = scrapy.Field()


class FansItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    uid = scrapy.Field()


class FollowersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    uid = scrapy.Field()


class ArtsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uid = scrapy.Field()
    id = scrapy.Field()
    attitudes_count = scrapy.Field()
    comments_count = scrapy.Field()
    created_at = scrapy.Field()
    reposts_count = scrapy.Field()
    source = scrapy.Field()
    text = scrapy.Field()
