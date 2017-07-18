# scrapy startproject dbdushu
import re
import scrapy
from ..items import BookItem
from bs4 import BeautifulSoup
from scrapy.http import Request


class doubanspider(scrapy.Spider):
    name = 'dbbook'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/']

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        for i in bs.find_all('a', href=re.compile('/tag/\w+')):
            url = 'https://book.douban.com' + i['href']
            yield Request(url, callback=self.parse1)

    def parse1(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        for i in bs.find_all('div', 'info'):
            item = BookItem()
            id_title = i.find('a', href=re.compile(
                'https://book.douban.com/subject'))
            link = id_title.get('href')
            item['id'] = re.search(r'\d+', link).group()
            item['title'] = id_title.get('title')
            item['pub'] = i.find('div', 'pub').get_text(strip=True)
            rate = i.find('span', 'rating_nums')
            num = i.find('span', 'pl')
            item['rate'] = rate.text if rate else None
            item['comments'] = num.get_text(strip=True) if num else None
            price = i.find('span', 'buy-info')
            item['price'] = price.get_text(strip=True)if price else None
            dec = i.find('p')
            item['dec'] = dec.get_text(strip=True) if dec else None
            yield (item)
        next_page = bs.find('a', text=re.compile(r'后页'))
        if next_page:
            next_url = 'https://book.douban.com' + next_page.get('href')
            print(next_url)
            yield Request(next_url, callback=self.parse1)
