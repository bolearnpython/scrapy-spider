# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from Proxy.items import ProxyItem
import ipdb


class ProxyPipeline(object):
    def open_spider(self, spider):
        self.con = redis.Redis()

    def process_item(self, item, spider):
        # ipdb.set_trace()
        if isinstance(item, ProxyItem):
            for ip in item['ip']:
                if self.con.zscore('proxies:all', ip):
                    if self.con.zscore('proxies:all', ip) < 0:
                        self.con.zadd('proxies:all', ip, 0)
                else:
                    self.con.zadd('proxies:all', ip, 0)
        else:
            pass
        return item
