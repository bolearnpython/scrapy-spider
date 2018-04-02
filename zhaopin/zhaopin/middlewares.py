# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

print(999999)

import ipdb


class Referer(object):

    def process_request(self, request, spider):
        referer = request.meta.get('referer', None)
        ipdb.set_trace()
        print(referer)
        if referer:
            request.headers['referer'] = referer
            print(referer)
        elif referer is 'https://www.lagou.com':
            request.headers['referer'] = referer
            print(referer)
