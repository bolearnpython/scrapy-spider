# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from Tmall.items import TmallItem
from scrapy.exceptions import DropItem
from scrapy_redis.BloomfilterOnRedis import BloomFilter


class TmallPipeline(object):
    def open_spider(self, spider):
        clinet = pymongo.MongoClient()
        db = clinet[spider.name]
        self.TmallItem = db['TmallItem']

    def process_item(self, item, spider):
        if isinstance(item, TmallItem):
            self.TmallItem.insert(item)
        else:
            pass
        return item


class TmallDuplicatesPipeline(object):
    def open_spider(self, spider):
        self.bf = BloomFilter(key='%s:dupefilter_item' % spider.name)

    def process_item(self, item, spider):
        if isinstance(item, TmallItem):
            fp = str(item['id'])
            if self.bf.isContains(fp):
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.bf.insert(fp)
                return item
        else:
            pass
        return item
