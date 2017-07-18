# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import logging
import string
from spider import make_random_useragent
class UserAgent(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = make_random_useragent("pc")
        request.headers["User-Agent"] = agent
        print(agent)

class Cookies(object):
    """ 换Cookie """
    def __init__(self):
        self.count=0
    def process_request(self, request, spider):
        self.count+=1
        if self.count%100==0:
            print('清理cookies'*8)
            request.cookies.clear()
            request.cookies={'bid': "".join(random.sample(string.ascii_letters + string.digits, 11))}