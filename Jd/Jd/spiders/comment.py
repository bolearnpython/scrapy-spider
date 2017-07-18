# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Jd.items import JdItem, Jd_Com_Item
from bs4 import BeautifulSoup
from scrapy import Request, Spider
import json
from furl import furl


class CommentSpider(Spider):
    name = 'comment'
    allowed_domains = ['jd.com']

    def start_requests(self):
        ID = '11960714890'
        url = 'https://item.jd.com/{id}.html'.format(id=ID)
        url_price = 'https://p.3.cn/prices/mgets?&skuIds=J_{id}'.format(id=ID)
        url_comments = 'https://club.jd.com/comment/productPageComments.action?productId={id}&score=0&sortType=5&page=1&pageSize=10'.format(
            id=ID)
        yield Request(url, meta={'id': ID})
        yield Request(url_price, meta={'id': ID}, callback=self.parse_price)
        yield Request(url_comments, callback=self.parse_comments,
                      meta={'page': 2, 'id': ID})

    def parse(self, response):
        _id = response.meta['id']
        bs = BeautifulSoup(response.text, 'lxml')
        param = bs.find('ul', 'parameter2 p-parameter-list')
        param = [item.text for item in param('li')]
        info = bs.find('div', 'itemInfo-wrap')
        title = info.find('div', 'sku-name').get_text(strip=True)
        yield JdItem({'title': title, 'param': param, '_id': _id})

    def parse_price(self, response):
        _id = response.meta['id']
        price = json.loads(response.text)[0]['p']
        yield JdItem({'price': price, '_id': _id})

    def parse_comments(self, response):
        if 'https://club.jd.com/comment/productPageComments.action' not in response.url:
            return
        _id = response.meta['id']
        data = json.loads(response.text)
        comment_hot = [(i['name'], i['count'])
                       for i in data['hotCommentTagStatistics']]
        lab_summary = {'afterCount', 'averageScore', 'commentCount', 'generalCount', 'generalRate',
                       'goodCount', 'goodRate', 'poorCount', 'poorRate', 'productId', 'showCount'}
        comment_pro = {i: data['productCommentSummary'][i]
                       for i in data['productCommentSummary'].keys() & lab_summary}
        for item in data['comments']:
            if 'images' in item:
                item['images'] = [i['imgUrl']for i in item['images']]
            lab_comments = {'content', 'creationTime', 'images', 'nickname', 'productColor', 'productSales',
                            'productSize', 'referenceName', 'referenceTime', 'score', 'userClientShow', 'userLevelName'}
            item_ = {i: item[i] for i in item.keys() & lab_comments}
            item_.update({'ID': _id})
            item_.update({'_id': item['id']})
            yield Jd_Com_Item(item_)
        if len(data['comments']) == 0:
            return
        yield JdItem({'comment_pro': comment_pro, 'comment_hot': comment_hot, '_id': _id})
        f_url_com = furl(response.url)
        page = response.meta['page']
        f_url_com.args['page'] = str(page)
        yield Request(f_url_com.url, meta={'page': page + 1, 'id': _id},
                      callback=self.parse_comments)
        for page in range(1, comment_pro['commentCount'] // 13):
            f_url_com.args['page'] = str(page)
            yield Request(f_url_com.url, meta={'page': page, 'id': _id},
                          callback=self.parse_comments)
