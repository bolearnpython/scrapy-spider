# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class ToutiaoPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient() 
        db = clinet["toutiao"]
        self.articles = db["articles"]
    def process_item(self, item, spider):
        self.articles.insert(dict(item))
        return item
