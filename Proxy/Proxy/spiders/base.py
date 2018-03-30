# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Proxy.items import ProxyItem
from bs4 import BeautifulSoup
from scrapy import Request, Spider
import re


class BaseSpider(Spider):
    name = 'base'
    allowed_domains = ['base.com']
    url1 = ['http://m.kuaidaili.com/free/inha/%d' % i for i in range(1, 5)]
    url2 = ['http://www.xicidaili.com/nn/%d' % i for i in range(1, 5)]
    url3 = ['http://www.mimiip.com/gngao/%d' % i for i in range(1, 5)]
    url4 = ['http://www.ip3366.net/free/?page=2', 'http://www.proxy360.cn/Region/China', 'http://www.ip181.com/daili/2.html',
            'http://www.89ip.cn/tiqv.php?tqsl=3000', 'http://www.iphai.com/free/ng']
    url5 = ['http://www.66ip.cn/areaindex_%d/%d.html' %
            (i, j)for i in range(1, 10)for j in range(1, 3)]
    start_urls = url1 + url2 + url3 + url4 + url5

    def parse(self, response):
        ips = re.findall(r'(\d+\.\d+\.\d+\.\d+)[^\d]+(\d+)', response.text)
        ips = {i[0] + ':' + i[1]for i in ips}
        yield ProxyItem({'ip': list(ips)})
