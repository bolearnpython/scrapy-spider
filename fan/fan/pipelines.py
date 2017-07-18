# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class FanPipeline(object):
    def open_spider(self, spider):
        clinet = pymongo.MongoClient()
        db = clinet['fan']
        self.fan = db['fan']

    def process_item(self, item, spider):
        try:
            self.fan.insert(dict(item))
        except:
            pass
        return item
