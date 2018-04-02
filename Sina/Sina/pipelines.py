# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem
from Sina.items import InfoItem, FansItem, FollowersItem, ArtsItem


class SinaPipeline(object):

    def open_spider(self, spider):
        clinet = pymongo.MongoClient()
        db = clinet['sina']
        self.InfoItem = db["InfoItem"]
        self.FansItem = db["FansItem"]
        self.FollowersItem = db["FollowersItem"]
        self.ArtsItem = db["ArtsItem"]

    def process_item(self, item, spider):
        if isinstance(item, ArtsItem):
            self.ArtsItem.insert(dict(item))
        elif isinstance(item, FollowersItem):
            self.FollowersItem.insert(dict(item))
        elif isinstance(item, FansItem):
            self.FansItem.insert(dict(item))
        elif isinstance(item, InfoItem):
            self.InfoItem.insert(dict(item))
        else:
            pass
        return item
