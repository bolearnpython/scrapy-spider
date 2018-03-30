# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Dangdang.items import DangdangItem
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
import ipdb


def take_first(x):
    return x[0]


class DangdangSpider(Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']

    def start_requests(self):
        url = 'http://category.dangdang.com/?ref=www-0-C'
        yield Request(url)

    def parse(self, response):
        for book_cate in response.css('div.classify_books'):
            cate = book_cate
            cate_name = cate.xpath('div/h3//text()').extract_first()
            for mini_cate in cate.css('div.classify_kind'):
                mini_cate_name = mini_cate.css(
                    'div.classify_kind_name a::text').extract_first()
                for detail in mini_cate.css('ul.classify_kind_detail a'):
                    detail_name = detail.xpath('text()').extract_first()
                    if '更多' not in detail_name:
                        url = detail.xpath('@href').extract_first()
                        print(cate_name, mini_cate_name, detail_name, url)
                        yield Request(url, callback=self.parse_index)

    def parse_index(self, response):
        # http://category.dangdang.com/cp01.04.07.00.00.00.html
        for book in response.css('div#search_nature_rg ul li'):
            loader = ItemLoader(item=DangdangItem(), selector=book)
            name_tag = loader.nested_css('p.name a')
            name_tag.add_xpath('href', '@href')
            name_tag.add_xpath('title', '@title')
            loader.add_css('price', 'p.price span::text')
            search_star_line = loader.nested_css('p.search_star_line')
            search_star_line.add_xpath(
                'star', 'span/span/@style', re=r'width: (\d+%)')
            search_star_line.add_xpath('comment', 'a//text()', re=r'(\d+)条评论')
            loader.add_css('search_shangjia', 'p.search_shangjia a::text')
            loader.add_css('search_shangjia_link',
                           'p.search_shangjia a::attr(href)')
            search_book_author = book.css(
                'p.search_book_author').xpath('span//text()').extract()
            loader.add_value('search_book_author',
                             search_book_author, take_first)
            yield loader.load_item()
        host_url = response.url.rsplit('/', maxsplit=1)[0]
        next_page = response.css('a[title=下一页]::attr(href)').extract_first()
        if next_page:
            url = host_url + next_page
            yield Request(url, callback=self.parse_index)
