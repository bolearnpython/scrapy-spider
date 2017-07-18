import re
from scrapy import Spider, Request
from bs4 import BeautifulSoup
from ..items import FanItem


class GanJi(Spider):
    name = 'ganji'
    start_urls = ['http://www.ganji.com/index.htm']

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        link_city_s = [(i['href'], i.text) for i in bs.find('dl')('a')]
        for link_city in link_city_s:
            for fangnb in ['fang1', 'fang5', 'fang12']:
                link, city = link_city
                link1 = link + fangnb
                yield Request(link1, meta={'link': link, 'fangnb': fangnb, 'city': city}, callback=self.parse1)

    def parse1(self, response):
        link, fangnb, city = response.meta['link'], response.meta[
            'fangnb'], response.meta['city']
        bs = BeautifulSoup(response.text, 'lxml')
        try:
            items = bs.find('div', 'listBox')('dl', 'list-img')
        except:
            try:
                items = bs.find('div', 'f-list')('dl', 'f-clear')
            except:
                return
        if not items:
            return
        for item in items:
            sale_item = FanItem()
            sale_item['_type'] = fangnb
            sale_item['name'] = city
            sale_item['img'] = item.find('img')['src']
            sale_item['title'] = item.find(
                'a', title=True).get_text(strip=True)
            sale_item['link'] = link[:-1] + item.find('a', href=True)['href']
            if fangnb == 'fang12':
                sale_item['address'] = item.find(
                    'p', 'list-word').get_text('|', strip=True).replace(' ', '')
                sale_item['detail'] = item.find(
                    'p', 'list-word pt-4').get_text(strip=True)
                sale_item['price'] = item.find(
                    'dd', 'fr col2').get_text('|', strip=True)
            else:
                sale_item['address'] = item.find(
                    'span', 'area').get_text(strip=True).replace(' ', '')
                sale_item['detail'] = item.find(
                    'dd', 'dd-item size').get_text('|', strip=True)
                sale_item['price'] = item.find(
                    'dd', 'dd-item info').get_text('|', strip=True)
            tags = item.find('dd', 'dd-item')
            sale_item['tags'] = tags.get_text(
                '|', strip=True) if tags else None
            yield sale_item
        if len(items) > 0:
            pages = bs('a', href=re.compile(r'^/%s/' %
                                            fangnb), text=re.compile(r'^\d{1,3}$'))
            for page in pages:
                Request(link[:-1] + page['href'], meta={
                        'link': link, 'fangnb': fangnb, 'city': city}, callback=self.parse1)
