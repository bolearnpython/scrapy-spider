# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Jd.items import JdItem, Item_Detail
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import SelectJmes
import json
from furl import furl


class JdSpider(Spider):
    name = 'jd'
    allowed_domains = ['jd.com']

    def start_requests(self):
        ID = '11960714890'
        url = 'https://item.jd.com/{id}.html'.format(id=ID)
        url_item = 'https://p.3.cn/prices/mgets?&skuIds=J_{id}'.format(id=ID)
        url_comments = 'https://club.jd.com/comment/productPageComments.action?productId={id}&score=0&sortType=5&page=1&pageSize=10'.format(
            id=ID)
        # yield Request(url, meta={'id': ID})
        yield Request(url_item, meta={'id': ID}, callback=self.parse_item)
        yield Request(url_comments, callback=self.parse_comments,
                      meta={'page': 2, 'id': ID})

    def parse_item(self, response):
        _id = response.meta['id']
        price = json.loads(response.text)[0]['p']
        yield Item_Detail({'price': price, '_id': _id})

    def parse_comments(self, response):
        if 'https://club.jd.com/comment/productPageComments.action' not in response.url:
            return
        _id = response.meta['id']
        data = json.loads(response.text)
        proc = SelectJmes("hotCommentTagStatistics[*].[name,count]")
        hot = proc(data)
        # for direct use on lists and dictionaries
        proc = SelectJmes(
            "productCommentSummary.[afterCount, averageScore, commentCount, generalCount, generalRate,goodCount, goodRate, poorCount, poorRate, productId, showCount]")
        product = proc(data)
        proc = SelectJmes(
            "comments[*].[images[*].imgUrl,content, creationTime, nickname, productColor, productSales,productSize, referenceName, referenceTime, score, userClientShow, userLevelName]")
        comments = proc(data)
        yield JdItem({'_id': _id, 'hot': hot, 'comments': comments, 'product': product})
        furl_page = furl(response.url)
        page = response.meta['page']
        furl_page.args['page'] = str(page)
        yield Request(furl_page.url, meta={'page': page + 1, 'id': _id},
                      callback=self.parse_comments)
        for page in range(1, product[2] // 13):
            furl_page.args['page'] = str(page)
            yield Request(furl_page.url, meta={'page': page, 'id': _id},
                          callback=self.parse_comments)
