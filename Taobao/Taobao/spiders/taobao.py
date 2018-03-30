# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Taobao.items import TaobaoItem
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, SelectJmes
import re
import json
from scrapy.loader.processors import SelectJmes
from w3lib.html import remove_tags


def strip_(value):
    if isinstance(value, str):
        return re.sub('\s', '', value)


def strip_x(value):
    if isinstance(value, str):
        return value.replace('\xa0', '')
    if isinstance(value, list):
        new_value = [i.replace('\xa0', '')for i in value]
        return new_value


class TaobaoSpider(Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com']

    def start_requests(self):
        itemId = '560129744052'
        url_count = 'http://rate.taobao.com/detailCount.do?itemId={itemId}'.format(
            itemId=itemId)
        yield Request(url_count, meta={'itemId': itemId})

    def parse(self, response):
        count = re.search(r'{"count":(\d+)}', response.text).group(1)
        itemId = response.meta['itemId']
        url_price = 'http://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId={itemId}&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,activity,fqg,zjys,couponActivity,soldQuantity,originalPrice,tradeContract&callback=onSibRequestSuccess'.format(
            itemId=itemId)
        headers = {'Host': 'detailskip.taobao.com',
                   'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
                   'Accept': '*/*',
                   'DNT': '1',
                   'Referer': 'http://item.taobao.com/item.htm?spm=a230r.1.14.20.10ab04acXM6tHe&id={itemId}&ns=1&abbucket=15'.format(itemId=itemId),
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.8,ko;q=0.6'}
        yield Request(url_price, headers=headers, callback=self.parse_price, meta={'itemId': itemId, 'count': count})

    def parse_price(self, response):
        itemId = response.meta['itemId']
        count = response.meta['count']
        data = re.findall('{.*}', response.text, re.S)[0]
        data = json.loads(data)['data']
        props = SelectJmes(
            "couponActivity.coupon.couponList[*].[icon,title,sellerId]")
        youhui = props(data)

        props = SelectJmes(
            "deliveryFee.data.[sendCity,serviceInfo.list[*].info]")
        kuaidi = props(data)

        props = SelectJmes("[price,promotion.promoData.[*][0][0][0].price]")
        price = props(data)
        info = (count, itemId, price, kuaidi, youhui)
        url = 'https://item.taobao.com/item.htm?id={itemId}'.format(
            itemId=itemId)
        yield Request(url, callback=self.parse_detail, meta={'info': info})

    def parse_detail(self, response):
        loader = ItemLoader(item=TaobaoItem(), response=response)
        loader.add_css(
            'shop', 'div.tb-shop-name a::attr(title)')
        loader.add_css(
            'shop_link', 'div.tb-shop-name a::attr(href)')
        loader.add_css('shop_rate', 'div.tb-shop-rate',
                       MapCompose(remove_tags, strip_))
        loader.add_css(
            'shop_sellor', 'div.tb-shop-seller a::text', MapCompose(strip_))
        loader.add_css('infos', 'ul.attributes-list li::text',
                       MapCompose(strip_x))
        loader.add_css('imgs', 'div.tb-item-info-l img::attr(data-src)')
        next_loader = loader.nested_css('div.tb-item-info-r')
        next_loader.add_css(
            'title', 'h3.tb-main-title::text', MapCompose(strip_))
        loader.add_value('info', response.meta['info'])
        yield loader.load_item()
