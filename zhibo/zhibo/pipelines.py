# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo 
from zhibo.items import ChannelItem, RoomItem
class ZhiboPipeline(object):
    def open_spider(self, spider):
        clinet = pymongo.MongoClient()
        site_setting = spider.settings.get('SITE')
        code=site_setting['code']
        db1 = clinet['zhibo1']
        db=db1[code]
        self.channel = db["ChannelItem"]
        self.room = db["RoomItem"]
        self.site=db1['Site']
        self.site.update({'code':code},dict(site_setting),upsert=True)

    def process_item(self, item, spider):
        if isinstance(item, RoomItem):
            self.room.update({'office_id':item['office_id']},dict(item),upsert=True)
        elif isinstance(item, ChannelItem):
            self.channel.update({'name':item['name']},dict(item),upsert=True)
        return item

