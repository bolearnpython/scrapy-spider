# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Sina.items import InfoItem, FansItem, FollowersItem, ArtsItem
from bs4 import BeautifulSoup
from scrapy import Request, Spider
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
        yield Request(url_art, meta={'uid': uid, 'page': page}, callback=self.parse_art)

    def parse_fans(self, response):
        uid = response.meta['uid']
        page = response.meta['page'] + 1
        cards_fans = json.loads(response.text)['cards'][0]['card_group']
        for card in cards_fans:
            info_fans = FansItem()
            if 'user' in card:
                user = card['user']
                info_fans['id'] = user['id']
                if user['id']:
                    uid = user['id']
                    page = 1
                    url_art = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=107603{uid}&page={page}'.format(
                        uid=uid, page=page)
                    yield Request(url_art, meta={'uid': uid, 'page': page}, callback=self.parse_art)
                info_fans['uid'] = uid
                yield info_fans
        url_fans = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&uid={uid}&page={page}'.format(
            uid=uid, page=page)
        if len(cards_fans) > 15:
            yield Request(url_fans, meta={'uid': uid, 'page': page}, callback=self.parse_fans)

    def parse_followers(self, response):
        uid = response.meta['uid']
        page = response.meta['page'] + 1
        cards_followers = json.loads(response.text)['cards'][0]['card_group']
        for card in cards_followers:
            if 'user' in card:
                user = card['user']
                info_followers = FollowersItem()
                info_followers['id'] = user['id']
                if user['id']:
                    uid = user['id']
                    page = 1
                    url_art = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=107603{uid}&page={page}'.format(
                        uid=uid, page=page)
                    yield Request(url_art, meta={'uid': uid, 'page': page}, callback=self.parse_art)
                info_followers['uid'] = uid
                yield info_followers
        url_followers = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&uid={uid}&page={page}'.format(
            uid=uid, page=page)
        if len(cards_followers) > 15:
            yield Request(url_followers, meta={'uid': uid, 'page': page}, callback=self.parse_followers)

    def parse_info(self, response):
        cards_info = json.loads(response.text)['cards']
        item = InfoItem()
        base = {}
        item['zu'] = []
        item['uid'] = response.meta['uid']
        item['base'] = base
        for card in cards_info:
            for info in card['card_group']:
                try:
                    name = info['item_name']
                    content = info['item_content']
                    base[name] = content
                except:
                    if 'item_type' in info:
                        _type = info['item_type']
                        content = info['item_content']
                        base[_type] = content
                    elif 'title_sub' in info:
                        lable = {'title_sub', 'card_expand',
                                 'desc1', 'desc2', 'pic'}
                        zu_info = {i: info[i]for i in info if i in lable}
                        item['zu'].append(zu_info)
                    continue
        yield item

    def parse_art(self, response):

        uid = response.meta['uid']
        page = response.meta['page']
        info_arts = json.loads(response.text)['cards']
        url_info = 'https://m.weibo.cn/api/container/getIndex?containerid=230283{uid}_-_INFO'.format(
            uid=uid)
        yield Request(url_info, meta={'uid': uid}, callback=self.parse_info)
        url_followers = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&uid={uid}&page={page}'.format(
            uid=uid, page=page)
        url_fans = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&uid={uid}&page={page}'.format(
            uid=uid, page=page)
        yield Request(url_followers, meta={'uid': uid, 'page': page}, callback=self.parse_followers)
        yield Request(url_fans, meta={'uid': uid, 'page': page}, callback=self.parse_fans)
        for art in info_arts:
            if 'mblog' in art:
                blog = art['mblog']
                info_art = {i: blog[i]for i in blog if i in [
                    'id', 'attitudes_count', 'comments_count', 'created_at', 'reposts_count', 'source', 'text']}
                info_art['uid'] = response.meta['uid']
                info_art = ArtsItem(info_art)
                yield info_art
            else:
                continue
