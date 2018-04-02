# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhipinItem(scrapy.Item):
    # define the fields for your item here like:
    job = scrapy.Field()
    salary = scrapy.Field()
    aera = scrapy.Field()
    work_year = scrapy.Field()
    edu = scrapy.Field()
    company_name = scrapy.Field()
    name_author = scrapy.Field()
    job_author = scrapy.Field()
    tags = scrapy.Field()
    job_time = scrapy.Field()
    industry = scrapy.Field()
    rongzi = scrapy.Field()
    people_num = scrapy.Field()


class DajieItem(scrapy.Item):
    # define the fields for your item here like:
    # name
    compHref = scrapy.Field()
    compName = scrapy.Field()
    imgSrc = scrapy.Field()
    industryName = scrapy.Field()
    jobHref = scrapy.Field()
    jobName = scrapy.Field()
    liHref = scrapy.Field()
    logoHref = scrapy.Field()
    pubCity = scrapy.Field()
    pubComp = scrapy.Field()
    pubEdu = scrapy.Field()
    pubEx = scrapy.Field()
    salary = scrapy.Field()
    scaleName = scrapy.Field()
    time = scrapy.Field()
