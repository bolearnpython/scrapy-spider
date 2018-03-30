# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from Vip.items import VipItem
from scrapy.exceptions import DropItem
from scrapy_redis.BloomfilterOnRedis import BloomFilter
import logging
logger = logging.getLogger(__name__)
logger.info('Pipeline called')

class VipPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        db = self.client[spider.name]
        self.VipItem = db['VipItem']

    def process_item(self, item, spider):
        if isinstance(item, VipItem):
            self.VipItem.insert(item)
        else:
            pass
        return item
    def close_spider(self, spider):
        self.client.close()

class VipDuplicatesPipeline(object):
    def open_spider(self, spider):
        self.bf = BloomFilter(key='%s:dupefilter_item' % spider.name)

    def process_item(self, item, spider):
        if isinstance(item, VipItem):
            fp = str(item['id'])
            if self.bf.isContains(fp):
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.bf.insert(fp)
                return item
        else:
            pass
        return item
