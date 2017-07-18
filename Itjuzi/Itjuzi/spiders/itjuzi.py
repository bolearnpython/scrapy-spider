# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Itjuzi.items import ItjuziItem
from bs4 import BeautifulSoup
from scrapy import Request, Spider


class ItjuziSpider(Spider):
    name = 'itjuzi'
    allowed_domains = ['itjuzi.com']

    def start_requests(self):
        for page in range(2, 60000):
            url = 'http://www.itjuzi.com/company/%s' % page
            yield Request(url)

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        try:
            title = bs.find(
                'h1', 'seo-important-title').get_text(strip=True).replace('\t', '')
        except:
            title = None
        try:
            slogan = bs.find('h2', 'seo-slogan').get_text(strip=True)
        except:
            slogan = None
        try:
            local = bs.find('span', 'loca c-gray-aset').get_text(strip=True)
        except:
            local = None
        try:
            scope = bs.find(
                'span', 'scope c-gray-aset').get_text(',', strip=True)
        except:
            scope = None
        try:
            link = bs.find('a', 'webTink')['href']
        except:
            link = None
        try:
            tags = bs.find('div', 'tagset').get_text(',', strip=True)
        except:
            tags = None
        try:
            des = bs.find('div', 'desc').get_text(',', strip=True)
        except:
            des = None
        try:
            des_more = bs.find('div', 'des-more').get_text(',', strip=True)
        except:
            des_more = None
        try:
            nb = bs.find(
                'div', 'block-numberpad colum3').get_text(',', strip=True)
        except:
            nb = None
        try:
            indus = [i.text.strip().split('\n')
                     for i in bs.find('div', 'sec indus-info')('tr')]
            indus_info = dict(zip(*indus))
        except:
            indus_info = None
        try:
            text_info = dict(i.get_text(strip=True).split('：')
                             for i in bs.find('ul', 'list-text-info')('li'))
        except:
            text_info = None
        try:
            company_number_in = [i.get_text('-', strip=True).split('-')
                                 for i in bs.find('div', 'sec institu-member')('div', 'right')]
        except:
            company_number_in = None
        try:
            company_number_out = [i.get_text('-', strip=True).split('-')
                                  for i in bs('div', 'sec institu-member')[-1]('div', 'right')]
        except:
            company_number_out = None
        try:
            product_info = [i.get_text('-', strip=True).split('-')for i in bs.find(
                'h2', text='产品信息').parent.parent('div', 'on-edit-hide')]
        except:
            product_info = None
        try:
            invst_info = [i.get_text('-', strip=True).split('-')
                          for i in bs.find('h2', text='获投信息').parent.parent('tr')]
        except:
            invst_info = None
        lab_result = [title, slogan, local, scope, link, tags, des, des_more, nb, indus_info,
                      text_info, company_number_in, company_number_out, product_info, invst_info]
        lab = ['title', 'slogan', 'local', 'scope', 'link', 'tags', 'des', 'des_more', 'nb', 'indus_info',
               'text_info', 'company_number_in', 'company_number_out', 'product_info', 'invst_info']

        item = ItjuziItem(dict(zip(lab, lab_result)))
        yield item
