# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from spider import make_random_useragent
# import random
# import cookies


# class CookiesMiddleware(object):
#     """ 换Cookie """

#     def process_request(self, request, spider):
#         cookie = random.choice(cookies)
#         request.cookies = cookie


class UserAgentMiddleware_pc(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        request.headers[
            "User-Agent"] = make_random_useragent(ua_type='pc')  #
        print(request.headers)


class UserAgentMiddleware_phone(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        request.headers[
            "User-Agent"] = make_random_useragent(ua_type='phone')


class UserAgentMiddleware_all(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        request.headers[
            "User-Agent"] = make_random_useragent()
