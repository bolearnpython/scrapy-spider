# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from Jd.items import JdItem, Jd_Com_Item
from scrapy.exceptions import DropItem
from scrapy_redis.BloomfilterOnRedis import BloomFilter


class JdPipeline(object):
    def open_spider(self, spider):
        clinet = pymongo.MongoClient()
        db = clinet[spider.name]
        self.JdItem = db['JdItem']
        self.Jd_Com_Item = db['Jd_Com_Item']

    def process_item(self, item, spider):
        if isinstance(item, JdItem):
            _id = self.JdItem.find({'_id': item['_id']})
            if len(list(_id)) == 0:
                self.JdItem.insert(item)
            self.JdItem.update({'_id': item['_id']}, {'$set': item})
        elif isinstance(item, Jd_Com_Item):
            self.Jd_Com_Item.insert(item)
        else:
            pass
        return item


class JdDuplicatesPipeline(object):
    def open_spider(self, spider):
        self.bf = BloomFilter(key='%s:dupefilter' % spider.name)

    def process_item(self, item, spider):
        if isinstance(item, Jd_Com_Item):
            fp = str(item['_id'])
            if self.bf.isContains(fp):
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.bf.insert(fp)
                return item
        else:
            pass
        return item
