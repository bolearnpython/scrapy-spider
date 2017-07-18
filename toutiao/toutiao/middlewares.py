# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


import random
from spider import make_random_useragent

Ua = [make_random_useragent(), make_random_useragent()]


class UserAgent(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(Ua)
