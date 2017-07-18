
import re
import ipdb
import logging
from bs4 import BeautifulSoup
from ..items import ZhipinItem
from scrapy import Request, Spider


class zhipin(Spider):
    name = 'zhipin'
    start_urls = ['https://www.zhipin.com']
    custom_settings = {
        'HTTPCACHE_ENABLED': False
    }

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        citys = {'上海', '深圳', '广州', '杭州', '成都', '重庆', '大连',
                 '南京', '武汉', '西安', '厦门', '长沙', '苏州', '天津'}
        job_type = [i.text for i in bs.find('div', 'job-menu')('a', href=True)]
        for job in job_type:
            for city in citys:
                url = 'https://www.zhipin.com/job_detail/?query=%s&city=%s' % (
                    job, city)
                yield Request(url, callback=self.parse1)

    def parse1(self, response):
        if response.status in [403, 302]:
            ipdb.set_trace()
        bs = BeautifulSoup(response.text, 'lxml')
        job_list = bs.find('div', 'job-list')
        if job_list:
            items = bs.find('div', 'job-list')('li')
            for item in items:
                _item = ZhipinItem()
                _item['job'], _item['salary'] = item.find('h3', 'name').strings
                _item['aera'], _item['work_year'], _item[
                    'edu'] = item.find('div', 'info-primary').p.strings
                _item['company_name'] = item.find(
                    'div', 'company-text').h3.text
                _item['name_author'], _item['job_author'], * \
                    _item['tags'] = item.find(
                        'div', 'job-tags').stripped_strings
                company_text = list(item.find('div', 'company-text').p.strings)
                has_time = item.find('div', 'job-time')
                _item['job_time'] = has_time.text if has_time else None
                if len(company_text) == 2:
                    company_text.insert(1, '')
                _item['industry'], _item['rongzi'], _item[
                    'people_num'] = company_text
                yield _item
        pages = bs.find('div', 'page')
        if pages:
            for tag in pages('a'):
                if 'javascript' not in tag['href']:
                    url = 'https://www.zhipin.com' + tag['href']
                    yield Request(url, callback=self.parse1)
