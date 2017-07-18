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


class LiepinItem(scrapy.Item):
    time = scrapy.Field()
    re_time = scrapy.Field()
    job = scrapy.Field()
    edu = scrapy.Field()
    aera = scrapy.Field()
    work_year = scrapy.Field()
    job_link = scrapy.Field()
    salary = scrapy.Field()
    company_name = scrapy.Field()
    company_link = scrapy.Field()
    industry = scrapy.Field()
    tags = scrapy.Field()


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    city = scrapy.Field()
    companyFullName = scrapy.Field()
    companyLabelList = scrapy.Field()
    companyLogo = scrapy.Field()
    companyShortName = scrapy.Field()
    companySize = scrapy.Field()
    createTime = scrapy.Field()
    education = scrapy.Field()
    positionId = scrapy.Field()
    financeStage = scrapy.Field()
    firstType = scrapy.Field()
    industryField = scrapy.Field()
    jobNature = scrapy.Field()
    positionAdvantage = scrapy.Field()
    positionName = scrapy.Field()
    salary = scrapy.Field()
    secondType = scrapy.Field()
    workYear = scrapy.Field()


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
