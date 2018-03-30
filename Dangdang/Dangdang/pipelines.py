# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from Dangdang.items import DangdangItem
from scrapy.exceptions import DropItem
from scrapy_redis.BloomfilterOnRedis import BloomFilter


class DangdangPipeline(object):
    def open_spider(self, spider):
        clinet = pymongo.MongoClient()
        db = clinet[spider.name]
        self.DangdangItem = db['DangdangItem']

    def process_item(self, item, spider):
        if isinstance(item, DangdangItem):
            self.DangdangItem.insert(item)
        else:
            pass
        return item


class DangdangDuplicatesPipeline(object):
    def open_spider(self, spider):
        self.bf = BloomFilter(key='%s:dupefilter_item' % spider.name)

    def process_item(self, item, spider):
        if isinstance(item, DangdangItem):
            fp = str(item['id'])
            if self.bf.isContains(fp):
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.bf.insert(fp)
                return item
        else:
            pass
        return item
