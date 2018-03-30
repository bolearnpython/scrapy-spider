# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from Zhihu.items import ZhihuItem
from scrapy.exceptions import DropItem
from scrapy_redis.BloomfilterOnRedis import BloomFilter
import logging
logger = logging.getLogger(__name__)
logger.info('Pipeline called')

class ZhihuPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        db = self.client[spider.name]
        self.ZhihuItem = db['ZhihuItem']

    def process_item(self, item, spider):
        if isinstance(item, ZhihuItem):
            self.ZhihuItem.insert(item)
        else:
            pass
        return item
    def close_spider(self, spider):
        self.client.close()

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
