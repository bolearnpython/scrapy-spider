from scrapy import Request, Spider
from bs4 import BeautifulSoup
import re
import ipdb
import logging
from ..items import FanItem


class Fan58(Spider):
    name = '58fan'
    start_urls = [
        'http://www.58.com/changecity.aspx?PGTID=0d200001-0019-ebac-1191-d89c9575f686&ClickID=2']
    headers = {'Cookie': 'f=n; id58=c5/njVkqOLmWNhzVC7k0Ag==',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'}

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        citys = [(i['href'], i.text)
                 for i in bs('a', href=re.compile(r'http://\w\w.58.com/'))]
        for city in citys:
            href, name = city
            url1 = href + 'chuzu/'
            url2 = href + 'ershoufang/'
            yield Request(url2, headers=self.headers, meta={'name': name, '_type': '二手房'}, callback=self.parse_ershou)
            yield Request(url1, headers=self.headers, meta={'name': name, '_type': '租房'}, callback=self.parse_zu)

    def parse_ershou(self, response):
        name = response.meta['name']
        _type = response.meta['_type']
        bs = BeautifulSoup(response.text, 'lxml')
        if bs.find('ul', 'house-list-wrap'):
            items = bs.find('ul', 'house-list-wrap')('li')
            for item in items:
                sale_item = FanItem()
                sale_item['name'] = name
                sale_item['_type'] = _type
                sale_item['img'] = item.find('img')['src']
                sale_item['title'] = item.find(
                    'h2', 'title').get_text(strip=True)
                sale_item['link'] = item.find('h2', 'title').a['href']
                details1, details2 = [i.get_text(',', strip=True).replace(
                    ' ', '').split(',') for i in item('p', 'baseinfo')]
                if len(details1) == 4:
                    [sale_item['zone'], sale_item['metter'], sale_item[
                        'cx'], sale_item['floor']] = details1
                elif len(details1) == 3:
                    [sale_item['zone'], sale_item['metter'],
                        sale_item['floor']] = details1
                else:
                    pass
                sale_item['address'] = details2[::-2]
                sale_item['price'], _, sale_item['price_one_metter'] = item.find(
                    'div', 'price').get_text(',', strip=True).split(',')
                sale_item['jjr'] = item.find(
                    'div', 'jjrinfo').get_text(',', strip=True)
                print(sale_item)
        next_page = bs.find('a', text='下一页')
        if next_page:
            yield Request(next_page['href'], meta={'name': name, '_type': _type}, headers=self.headers, callback=self.parse_ershou)

    def parse_zu(self, response):
        name = response.meta['name']
        _type = response.meta['_type']
        bs = BeautifulSoup(response.text, 'lxml')
        if bs.find('ul', 'listUl'):
            items = bs.find('ul', 'listUl')('li', sortid=True)
            for item in items:
                sale_item = FanItem()
                sale_item['name'] = name
                sale_item['_type'] = _type
                sale_item['img'] = item.find('img')['src']
                sale_item['title'] = item.find('h2').get_text(strip=True)
                sale_item['zone'], sale_item['metter'] = re.sub(
                    r'\s+', ',', item.find('p', 'room').text).split(',')
                sale_item['address'] = re.sub(
                    r'\s+', ',', item.find('p', 'add').text).strip(',').split(',')
                sale_item['price_one_month'] = item.find(
                    'div', 'money').get_text(',', strip=True)
                jjr = item.find('span', ' jjr_par')
                if jjr:
                    sale_item['jjr'] = re.sub(r'\s+', ',', jjr.text).strip(',')
                print(sale_item)
        next_page = bs.find('a', text='下一页')
        if next_page:
            yield Request(next_page['href'], meta={'name': name, '_type': _type}, headers=self.headers, callback=self.parse_zu)
