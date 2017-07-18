import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
from furl import furl
s = requests.Session()
url = 'https://nanzhuang.tmall.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
response = s.get(url, headers=headers)
bs = BeautifulSoup(response.text, 'lxml')
url_list = bs('a', href=re.compile(
    r'.*list.tmall.com/search_product.htm.*'))
url_list = ['https:' + i['href'] for i in url_list]


def parse_list(url):
    response = s.get(url, headers=headers)
    bs = BeautifulSoup(response.text, 'lxml')
    for item in bs('div', 'product'):
        item_link = item.find('a', href=re.compile(
            r'//detail.tmall.com/item.htm.*'))
        item_price = item.find('p', 'productPrice')
        item_title = item.find('p', 'productTitle')
        item_shop = item.find('a', 'productShop-name')
        item_status = item.find('p', 'productStatus')
        item_info = {}
        if item_price:
            item_info['price'] = item_price.get_text(strip=True)
        if item_link:
            item_info['link'] = item_link['href']
        if item_title:
            item_info['title'] = item_title.get_text(strip=True)
        if item_shop:
            item_info['shop_name'] = item_shop.get_text(strip=True)
            item_info['shop_link'] = item_shop['href']
        if item_status:
            item_info['shop_nb'], item_info['shop_com_nb'], * \
                _ = [i.text for i in item_status.select('span')]
        print(item_info)
        if 'link' in item_info:
            url = 'https:' + item_info['link']
            parse_item(url)


def parse_item(url):
    b = furl('https://aldcdn.tmall.com/recommend.htm?itemId=531841713885&sellerId=849905958&rn=bffe2de31b3d7b92b00a65895405b6d4&appId=03054')
    a = furl(url)
    b.args['sellerId'] = a.args['user_id']
    b.args['itemId'] = a.args['id']
    b.args['rn'] = a.args['rn']
    url = b.url
    r = s.get(url, headers=headers)
    print(r.json())


with ThreadPoolExecutor(10) as executor:
    for url in url_list:
        executor.submit(parse_list, url)
        # https://rate.tmall.com/list_detail_rate.htm?itemId=35303514363&sellerId=696169594&order=3&currentPage=1
