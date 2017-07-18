import re
import ipdb
import logging
from scrapy import Request, Spider
from bs4 import BeautifulSoup
from ..items import FanItem


class FanTianXia(Spider):
    name = 'fantianxia'
    start_urls = ['http://fang.com/SoufunFamily.htm']

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        citys = [(i['href'], i.text)
                 for i in bs('a', href=re.compile(r'http://\w+.fang.com/'))]
        for city in citys:
            href, name = city
            url1 = href.replace('//', '//esf.')
            url2 = href.replace('//', '//newhouse.')
            url3 = href.replace('//', '//zu.')
            yield Request(url3, meta={'name': name, 'url': url3.strip('/'), '_type': '租房'}, callback=self.parse_zu)
            yield Request(url2 + 'house/s/', meta={'name': name, 'url': url2.strip('/'), '_type': '新房'}, callback=self.parse_new)
            yield Request(url1, meta={'name': name, 'url': url1.strip('/'), '_type': '二手房'}, callback=self.parse_ershou)

    def parse_ershou(self, response):
        name = response.meta['name']
        url = response.meta['url']
        _type = response.meta['_type']
        bs = BeautifulSoup(response.text, 'lxml')
        if bs.find('div', 'houseList'):
            items = bs.find('div', 'houseList')('dl', 'list rel')
            for item in items:
                sale_item = FanItem()
                sale_item['name'] = name
                sale_item['_type'] = _type
                sale_item['link'] = url + item.find('a')['href']
                sale_item['img'] = item.find('a').img['src']
                temp = item.find('dd', 'info rel floatr').contents[1::2]
                details = [i.get_text(strip=True) for i in temp]
                sale_item['title'], temp1, sale_item['address'], fangzhu, sale_item[
                    'tags'], sale_item['metter'], price_temp = details
                temp1 = temp1.split('|')
                if len(temp1) == 4:
                    sale_item['zone'], sale_item['floor'], sale_item[
                        'cx'], sale_item['build_time'] = temp1
                elif len(temp1) == 3:
                    sale_item['zone'], sale_item[
                        'floor'], sale_item['build_time'] = temp1
                else:
                    pass
                print(sale_item)
        next_page = bs.find('a', text='下一页')
        if next_page:
            yield Request(url + next_page['href'], meta={'name': name, 'url': url, '_type': _type}, callback=self.parse_ershou)

    def parse_new(self, response):
        name = response.meta['name']
        url = response.meta['url']
        _type = response.meta['_type']
        bs = BeautifulSoup(response.text, 'lxml')
        if bs.find('div', 'nhouse_list'):
            items = bs.find('div', 'nhouse_list')('li')
            for item in items:
                try:
                    sale_item = FanItem()
                    sale_item['_type'] = _type
                    sale_item['name'] = name
                    sale_item['link'] = item.find('a')['href']
                    sale_item['img'] = item.find('img')['src']
                    sale_item['title'] = item.find(
                        'div', 'nlcd_name').get_text(strip=True)
                    sale_item['zone'], sale_item['metter'] = item.find(
                        'div', 'house_type').get_text(strip=True).replace('\t', '').split('－\n')
                    sale_item['address'] = item.find(
                        'div', 'address').get_text(strip=True).replace('\t', '')
                    sale_item['tags'] = item.find('div', 'fangyuan').get_text(
                        ',', strip=True).split(',')
                    sale_item['price_one_metter'] = item.find(
                        'div', 'nhouse_price').text if item.find('div', 'nhouse_price') else None
                    print(sale_item)
                except:
                    pass
        next_page = bs.find('a', text='下一页')
        if next_page:
            yield Request(url + next_page['href'], meta={'name': name, 'url': url, '_type': _type}, callback=self.parse_new)

    def parse_zu(self, response):
        name = response.meta['name']
        bs = BeautifulSoup(response.text, 'lxml')
        _type = response.meta['_type']
        url = response.meta['url']
        if bs.find('div', 'houseList'):
            items = bs.find('div', 'houseList')('dl')
            for item in items:
                sale_item = FanItem()
                sale_item['name'] = name
                sale_item['_type'] = _type
                sale_item['link'] = url + item.find('a')['href']
                sale_item['img'] = item.find('img')['src']
                temp = item.find('dd', 'info rel').contents[1:-7:2]
                details = [i.get_text(strip=True) for i in temp]
                sale_item['title'], temp1, sale_item['address'], sale_item['bus'], sale_item[
                    'update_time'], sale_item['tags'], sale_item['price_one_month'] = details
                temp1 = temp1.split('|')
                if len(temp1) == 5:
                    sale_item['zu_type'], sale_item['zone'], sale_item[
                        'metter'], sale_item['floor'], sale_item['cx'] = temp1
                elif len(temp1) == 4:
                    sale_item['zone'], sale_item['metter'], sale_item[
                        'floor'], sale_item['cx'] = temp1
                print(sale_item)
        next_page = bs.find('a', text='下一页')
        if next_page:
            yield Request(url + next_page['href'], meta={'name': name, 'url': url, '_type': _type}, callback=self.parse_zu)
