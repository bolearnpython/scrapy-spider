
import re
import ipdb
import scrapy
import requests
from scrapy import log
from scrapy.http import Request
from bs4 import BeautifulSoup
from ..items import FanItem


class DmozSpider(scrapy.Spider):
    name = "anjuke"
    allowed_domains = ['www.anjuke.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 5
    }

    def start_requests(self):
        root_url = "http://www.anjuke.com/sy-city.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'}
        r = requests.get(root_url, headers)
        bs = BeautifulSoup(r.text, 'lxml')
        a = [(i['href'], i.text)
             for i in bs.find("div", ["left_side", "right_side"])('a')]
        for url_city in a:
            url, city = url_city
            yield Request(url + '/sale', headers={'Referer': url}, meta={'city': city}, callback=self.parser1)

    def parser1(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        city = response.meta['city']
        for item in bs('li', 'list-item'):
            sale_item = FanItem()
            sale_item['name'] = city
            sale_item['_type'] = '二手房'
            sale_item['img'] = item.find('img')['src']
            sale_item['title'] = item.find('a', href=True).get_text(strip=True)
            sale_item['link'] = item.find('a', href=True)['href']
            sale_item['address'] = item.find('span', 'comm-address')['title'].replace(
                '\xa0', ' ') if item.find('span', 'comm-address') else None
            sale_item['detail'] = item.find(
                'div', 'details-item').get_text(strip=True)
            try:
                sale_item['tags'] = item.find('span', 'broker-name').text
            except:
                sale_item['tags'] = None
            yield sale_item
        return
        zu_a = bs.find('ul', 'L_tabsnew').find(
            'a', href=re.compile(r'zu\.anjuke\.com'))
        if zu_a:
            yield Request(zu_a['href'], meta={'city': city}, callback=self.parser2)
        fang_a = bs.find('ul', 'L_tabsnew').find(
            'a', href=re.compile(r'fang\.anjuke\.com'))
        if fang_a:
            yield Request(fang_a['href'], meta={'city': city}, callback=self.parser3)
        nextpage = bs.find('a', text=re.compile('下一页'))
        if nextpage:
            yield Request(nextpage['href'], meta={'city': city}, callback=self.parser1)

    def parser2(self, response):
        '''租房'''
        bs1 = BeautifulSoup(response.text, 'lxml')
        city = response.meta['city']
        for item in bs1('div', 'zu-itemmod'):
            zu_item = FanIte()
            zu_item['name'] = city
            zu_item['_type'] = '租房'
            zu_item['link'] = item.a.attrs['href']
            zu_item['title'] = item.a.attrs['title']
            zu_item['detail'] = item.find('p', 'details-item tag').text
            zu_item['address'] = item.find(
                'address', 'details-item').get_text(strip=True).replace('\xa0', ' ')
            zu_item['tags'] = item.find(
                'p', 'details-item bot-tag').get_text(strip=True)
            zu_item['price'] = item.find('div', 'zu-side').get_text(strip=True)
            yield zu_item
        nextpage = bs1.find('a', text=re.compile('下一页'))
        if nextpage:
            yield Request(nextpage['href'], meta={'city': city}, callback=self.parser2)

    def parser3(self, response):
        '''新房'''
        city = response.meta['city']
        bs2 = BeautifulSoup(response.text, 'lxml')
        try:
            items = bs2.find('div', 'key-list')('div', 'item-mod')
        except:
            return
        for item in items:
            xm_item = FanItem()
            xm_item['_type'] = '新房'
            xm_item['name'] = city
            xm_item['title'] = item.find('a', 'items-name').text
            xm_item['address'] = item.find('p', 'address').get_text(
                strip=True).replace('\xa0', ' ')
            try:
                xm_item['zone'] = item.find(
                    text=re.compile("户")).parent.get_text(strip=True)
            except:
                xm_item['zone'] = None
            xm_item['price'] = item.find(
                'p', 'price').text if item.find('p', 'price') else None
            yield xm_item
        nextpage = bs2.find('a', text=re.compile('下一页'))
        if nextpage:
            yield Request(nextpage['href'], meta={'city': city}, callback=self.parser3)
