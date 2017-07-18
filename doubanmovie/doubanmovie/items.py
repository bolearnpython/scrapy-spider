# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmovieItem(scrapy.Item):
    url= scrapy.Field()
    name= scrapy.Field()
    year= scrapy.Field()
    img= scrapy.Field()
    movie_info= scrapy.Field()
    rate= scrapy.Field()
    rate_people= scrapy.Field()
    rating_per_list= scrapy.Field()