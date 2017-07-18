
import re
import ipdb
import logging
import json
from bs4 import BeautifulSoup
from ..items import LiepinItem
from scrapy import Request, Spider


class LiePin(Spider):
    name = 'liepin'
    base_url = 'https://www.liepin.com'
    start_urls = ['https://www.liepin.com/it/']

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        jobs = bs.find('ul', 'sidebar float-left')('a')
        for job in jobs:
            url = self.base_url + job['href']
            name = job.text
            yield Request(url, callback=self.parse1)

    def parse1(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        if bs.find('ul', 'sojob-list'):
            items = bs.find('ul', 'sojob-list')('li')
            for item in items:
                _item = LiepinItem()
                job_info = item.find('div', 'job-info')
                company_info = item.find('div', 'company-info nohover')
                _item['job'] = job_info.h3.get_text(strip=True)
                _item['edu'] = job_info.p.find('span', 'edu').text
                _item['aera'] = job_info.p.find('a', 'area').text
                _item['work_year'] = job_info.p.select('span')[-1].text
                _item['job_link'] = job_info.h3.a['href']
                _item['salary'] = job_info.p.find('span', 'text-warning').text
                company_name = company_info.find('p', 'company-name')
                _item['company_name'] = company_name.get_text(strip=True)
                try:
                    _item['company_link'] = company_name.a['href']
                except:
                    pass
                _item['industry'] = company_info.find(
                    'a', 'industry-link').text
                _item['tags'] = company_info.find(
                    'p', 'temptation clearfix').get_text(',', strip=True)
                _time = item.find('p', 'time-info clearfix')
                _item['time'] = _time.time.text
                _item['re_time'] = _time.span.text
                yield _item

        next_page = bs.find('a', text='下一页')
        if next_page:
            url = next_page['href']
            yield Request(url, callback=self.parse1)
