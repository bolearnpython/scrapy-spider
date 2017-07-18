# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



import pymongo 
from doubanmovie.items import DoubanmovieItem
class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient()
        db = clinet["doubanmovie"]
        self.doubanmovie = db["DoubanmovieItem"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, DoubanmovieItem):
            try:
                self.doubanmovie.insert(dict(item))
            except Exception:
                pass
        return item
