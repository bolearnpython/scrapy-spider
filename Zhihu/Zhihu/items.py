# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # id = scrapy.Field() #过滤
    columnsCount = scrapy.Field()
    followingTopicCount = scrapy.Field()
    headline = scrapy.Field()
    questionCount = scrapy.Field()
    answerCount = scrapy.Field()
    favoritedCount = scrapy.Field()
    employments = scrapy.Field()
    description = scrapy.Field()
    voteupCount = scrapy.Field()
    participatedLiveCount = scrapy.Field()
    followerCount = scrapy.Field()
    followingCount = scrapy.Field()
    followingColumnsCount = scrapy.Field()
    followingQuestionCount = scrapy.Field()
    locations = scrapy.Field()
    educations = scrapy.Field()
    articlesCount = scrapy.Field()
    name = scrapy.Field()
    favoriteCount = scrapy.Field()
    followingFavlistsCount = scrapy.Field()
    thankedCount = scrapy.Field()
    business = scrapy.Field()
    logsCount = scrapy.Field()
