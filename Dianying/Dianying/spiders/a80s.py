# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Dianying.items import DianyingItem
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, SelectJmes

class A80sSpider(Spider):
    name = '80s'
    allowed_domains = ['80s.com']

    def start_requests(self):
        url = 'http://80s.com/'
        yield Request(url)

    def parse(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
#        url=
#        yield Request(url,callback=self.parse_item)
    def parse_item(self,response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        #proc = SelectJmes("e.{Name: name, State: state.name}.a[name, state.name].b[?state=='running'].c[0:5:-1].d[1][0].people[*].first[] | [0]")
        #length(people)max_by(people, &age)[?contains(@, 'foo') == `true`]
        #proc({'foo': 'bar'})
        css = None
        name = None
        select_ul=response.css(css)
        if select_ul:
            for select_item in select_ul:
                loader = ItemLoader(item=DianyingItem(), selector=select_item)
                loader.add_css(name, css)
                next_loader = loader.nested_css(next_css)
                next_loader.add_css(name,css,TakeFirst(), unicode.title, re='*')
                yield loader.load_item()
        else:
            self.logger.info('没有对应selector,parse_item on %s ', response.url)
#        url=
#        yield Request(url,callback=self.parse_detail)
    def parse_detail(self,response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        loader = ItemLoader(item=DianyingItem(), response=response)
        loader.add_css(name, css)
        next_loader = loader.nested_css(next_css)
        yield loader.load_item()
