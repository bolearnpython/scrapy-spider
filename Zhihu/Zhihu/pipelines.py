# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from Zhihu.items import ZhihuItem
from scrapy.exceptions import DropItem
from scrapy_redis.BloomfilterOnRedis import BloomFilter


class ZhihuPipeline(object):
    def open_spider(self, spider):
        clinet = pymongo.MongoClient()
        db = clinet[spider.name]
        self.ZhihuItem = db['ZhihuItem']

    def process_item(self, item, spider):
        if isinstance(item, ZhihuItem):
            self.ZhihuItem.insert(item)
        else:
            pass
        return item


class ZhihuDuplicatesPipeline(object):
    def open_spider(self, spider):
        self.bf = BloomFilter(key='%s:dupefilter_item' % spider.name)

    def process_item(self, item, spider):
        if isinstance(item, ZhihuItem):
            fp = str(item['id'])
            if self.bf.isContains(fp):
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.bf.insert(fp)
                return item
        else:
            pass
        return item
