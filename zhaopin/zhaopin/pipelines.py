# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
import ipdb
from zhaopin.items import ZhipinItem, LiepinItem, LagouItem, DajieItem


class ZhaopinPipeline(object):
    def open_spider(self, spider):
        clinet = pymongo.MongoClient()
        db = clinet['zhaopin']
        self.Zhipin = db["ZhipinItem"]
        self.Liepin = db["LiepinItem"]
        self.Lagou = db['LagouItem']
        self.Dajie = db['DajieItem']

    def process_item(self, item, spider):
        if isinstance(item, ZhipinItem):
            self.Zhipin.insert(dict(item))
        elif isinstance(item, LiepinItem):
            self.Liepin.insert(dict(item))
        elif isinstance(item, LagouItem):
            self.Lagou.update(
                {'positionId': item['positionId']}, dict(item), upsert=True)
        elif isinstance(item, DajieItem):
            self.Dajie.insert(dict(item))
        else:
            ipdb.set_trace()
        return item
