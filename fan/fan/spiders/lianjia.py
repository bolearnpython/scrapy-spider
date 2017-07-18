
import re
import ipdb
import logging
from bs4 import BeautifulSoup
from ..items import FanItem
from scrapy import Request, Spider


class LianJia(Spider):
    name = 'lianjia'
    start_urls = ['http://sh.lianjia.com/']

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        name = 'sh'
        yield Request('http://sh.lianjia.com/zufang', meta={'page': 2, 'name': name, 'url': 'http://sh.lianjia.com/zufang'}, callback=self.parse_zu)
        yield Request('http://sh.fang.lianjia.com/loupan', meta={'page': 2, 'name': name, 'url': 'http://sh.fang.lianjia.com/'}, callback=self.parse_new)
        yield Request('http://sh.lianjia.com/ershoufang/', meta={'page': 2, 'name': name, 'url': 'http://sh.lianjia.com/'}, callback=self.parse_sh)
        for city in bs.find("div", "cityList clear")("a"):
            url, name = city['href'], city.text
            yield Request(url, meta={'name': name}, callback=self.parse_city)

    def parse_city(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        name = response.meta['name']
        ershou = bs.find('a', text='二手房')
        if ershou:
            yield Request(ershou['href'], meta={'page': 2, 'name': name, 'url': ershou['href']}, callback=self.parse_ershou)
        new = bs.find('a', text='新房')
        if new:
            yield Request(new['href'] + 'loupan', meta={'page': 2, 'name': name, 'url': new['href']}, callback=self.parse_new)
        zu = bs.find('a', text='租房')
        if zu:
        yield Request(zu['href'], meta={'page': 2, 'name': name, 'url': zu['href']}, callback=self.parse_zu)

    def parse_sh(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        print(response.url)
        items = bs.find('div', 'm-list').ul('li')
        for item in items:
            url = 'http://sh.lianjia.com' + item.a['href']
            img = item.a.img['src']
            title = item.a.img['alt']
            prices = item.find(
                'div', 'info-col price-item main').get_text(strip=True)
            price = item.find(
                'span', 'info-col price-item minor').get_text(strip=True)
            tags = item.find(
                'div', 'property-tag-container').get_text(',', strip=True)
            temp1, temp2, price = [i.get_text(
                strip=True)for i in item('span', 'info-col')]
            *where, time = temp2.split('|')
            temp1_list = temp1.split('|')
            if len(temp1_list) == 4:
                zone, meters, flood, cx = temp1_list
            elif len(temp1_list) == 3:
                zone, meters, flood = temp1_list
                cx = ''
            meters = re.sub(r'\s', '', meters)
            ershou_info = {'url': url, 'img': img, 'title': title, 'prices': prices, 'price': price,
                           'tags': tags, 'where': where, 'time': time, 'zone': zone, 'meters': meters, 'cx': cx}
            print(ershou_info)
        page = response.meta['page']
        response.meta['page'] += 1
        if len(items) > 0:
            yield Request(response.meta['url'] + 'ershoufang/pg%d' % page, meta=response.meta, callback=self.parse_ershou_sh)

    def parse_new(self, response):
        print(response.url + response.meta['name'])
        bs = BeautifulSoup(response.text, 'lxml')
        prices = [i.get_text(strip=True) for i in bs('div', 'price')]
        imgs = [i.find('img')['src']for i in bs('div', 'pic-panel')]
        for price, img, item in zip(prices, imgs, bs('div', 'col-1')):
            new_info = FanItem()
            new_info['_type'] = '新房'
            new_info['name'] = response.meta['name']
            title, where, zone_meter, _type = [j.get_text(
                ',', strip=True) for i, j in enumerate(item.contents) if i % 2 != 0]
            new_dict = dict(zip(['title', 'address', 'zone', 'tags', 'img', 'price'], [
                            title, where, zone_meter, _type, img, price]))
            new_info.update(new_dict)
            yield new_info
        page = response.meta['page']
        response.meta['page'] += 1
        if len(imgs) > 0:
            yield Request(response.meta['url'] + 'loupan/pg%d' % page, meta=response.meta, callback=self.parse_new)

    def parse_ershou(self, response):
        print(response.url + response.meta['name'])
        bs = BeautifulSoup(response.text, 'lxml')
        page = response.meta['page']
        response.meta['page'] += 1
        items = bs.find('ul', 'sellListContent')('li')
        for item in items:
            sale_item = FanItem()
            sale_item['_type'] = '二手房'
            sale_item['link'] = item.a['href']
            sale_item['name'] = response.meta['name']
            sale_item['img'] = item.a.img['src']
            sale_item['title'], sale_item['detail'], sale_item['floor'], sale_item['follow'], sale_item[
                'tags'], sale_item['price'] = [i.get_text(',', strip=True) for i in item.find('div', 'info clear').contents]
            yield sale_item
        page = response.meta['page']
        response.meta['page'] += 1
        if len(items) > 0:
            yield Request(response.meta['url'] + '/pg%d' % page, meta=response.meta, callback=self.parse_ershou)

    def parse_zu(self, response):
        print(response.url + response.meta['name'])
        province = response.meta['name']
        bs = BeautifulSoup(response.text, 'lxml')
        items = bs.find_all('div', 'info-panel')
        for item in items:
            zu_info = FanItem()
            zu_info['_type'] = '租房'
            zu_info['name'] = response.meta['name']
            info = [zu_info.setdefault(x, y)for x, y in zip(
                ('address', 'zone', 'metter', 'cx'), item.find('div', 'where').stripped_strings)]
            info1 = item.find('a').attrs
            zu_info['title'] = info1['title']
            re.match(info1['href'], r'lianjia\.com/zufang/')
            zu_info['link'] = info1['href']if re.match(
                r'.*lianjia.*', info1['href'])else 'http://%s.lianjia.com' % province + info1['href']
            [zu_info.setdefault(i, j.text)for i, j in zip(
                ['price', 'follow'], item.find_all('span', 'num'))]
            info2 = item.find('div', 'con').get_text(strip=True)
            aera_floor = info2.split('|') if len(
                info2.split('|'))is 3 else info2.split('/')
            if len(info) is 4:
                [zu_info.setdefault(x, y)for x, y in zip(
                    ['address', 'floor', 'build_time'], aera_floor)]
            elif len(info) is 3:
                [zu_info.setdefault(x, y)for x, y in zip(
                    ['address', 'floor', 'cx'], aera_floor)]
            zu_info['price'] = item.find('div', 'price').get_text(strip=True)
            try:
                zu_info['update_time'] = re.search(
                    r'\d+\.\d+\.\d+', item.find('div', 'price-pre').text).group()
            except:
                print('Not find time')
            yield zu_info
        page = response.meta['page']
        response.meta['page'] += 1
        if len(items) > 0:
            yield Request(response.meta['url'] + '/pg%d' % page, meta=response.meta, callback=self.parse_zu)
