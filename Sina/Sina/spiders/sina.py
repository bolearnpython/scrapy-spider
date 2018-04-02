# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Sina.items import InfoItem, FansItem, FollowersItem, ArtsItem
from bs4 import BeautifulSoup
from scrapy import Request, Spider
from scrapy.loader.processors import SelectJmes
import json
import ipdb


class SinaSpider(Spider):
    name = 'sina'
    allowed_domains = ['weibo.cn']

    def start_requests(self):
        uid = '6008806694'
        page = 1
        url_art = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=107603{uid}&page={page}'.format(
            uid=uid, page=page)
        url_info = 'https://m.weibo.cn/api/container/getIndex?containerid=230283{uid}_-_INFO'.format(
            uid=uid)
        url_followers = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&uid={uid}&page={page}'.format(
            uid=uid, page=page)
        url_fans = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&uid={uid}&page={page}'.format(
            uid=uid, page=page)
        yield Request(url_info, meta={'uid': uid}, callback=self.parse_info)
        yield Request(url_art, meta={'uid': uid, 'page': page}, callback=self.parse_art)
        yield Request(url_followers, meta={'uid': uid, 'page': page}, callback=self.parse_followers)
        yield Request(url_fans, meta={'uid': uid, 'page': page}, callback=self.parse_fans)

    def parse_fans(self, response):
        uid = response.meta['uid']
        page = response.meta['page'] + 1
        fans_item = SelectJmes(
            'data.cards[0].card_group[*].user.[id,screen_name,statuses_count,description,followers_count,follow_count]')
        fans_item = fans_item(json.loads(response.text))
        print(fans_item)

    def parse_followers(self, response):
        uid = response.meta['uid']
        page = response.meta['page'] + 1
        follower_item = SelectJmes(
            'data.cards[0].card_group[*].user.[id,screen_name,statuses_count,description,followers_count,follow_count]')
        follower_item = follower_item(json.loads(response.text))
        print(follower_item)

    def parse_info(self, response):
        info_item = SelectJmes(
            'data.cards[0].card_group[*].[item_name,item_content]')
        info_item = info_item(json.loads(response.text))
        print(info_item)

    def parse_art(self, response):
        item = SelectJmes(
            'data.cards[0].mblog.[id,attitudes_count,comments_count,created_at,reposts_count]')
        item = item(json.loads(response.text))
        print(item)
