# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from Itjuzi.items import ItjuziItem
from scrapy.exceptions import DropItem
from scrapy_redis.BloomfilterOnRedis import BloomFilter


class ItjuziPipeline(object):
    def open_spider(self, spider):
        clinet = pymongo.MongoClient()
        db = clinet[spider.name]
        self.ItjuziItem = db['ItjuziItem']

    def process_item(self, item, spider):
        if isinstance(item, ItjuziItem):
            self.ItjuziItem.insert(dict(item))
        else:
            pass
        return item


class ItjuziDuplicatesPipeline(object):
    def open_spider(self, spider):
        self.bf = BloomFilter(key='%s:dupefilter_item' % spider.name)

    def process_item(self, item, spider):
        if isinstance(item, ItjuziItem):
            fp = str(item['title'])
            if self.bf.isContains(fp):
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.bf.insert(fp)
                return item
        else:
            pass
        return item
