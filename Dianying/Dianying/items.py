# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


def make_(value):
    for i, j in enumerate(value):
        if '◎简介' in j:
            jianjie_index = i
        if '◎主演' in j:
            zuyan_index = i
    l1 = value[:zuyan_index]
    l2 = value[zuyan_index:jianjie_index]
    l3 = value[jianjie_index:-2]
    l4 = value[-2:]
    return l1 + [''.join(l2), ''.join(l3), ':'.join(l4)]


class DianyingItem(scrapy.Item):
    # define the fields for your item here like:
    # id = scrapy.Field() #过滤
    info = scrapy.Field()
