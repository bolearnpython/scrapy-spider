import re
import ipdb
import logging
import json
from bs4 import BeautifulSoup
from ..items import DajieItem
from scrapy import Request, Spider


class DaJie(Spider):
    name = 'dajie'
    start_urls = ['https://job.dajie.com/']
    custom_settings = {
        'HTTPCACHE_ENABLED': True,
    }

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        jobs = bs.find(text=re.compile('产品/技术')).parent.parent('a')
        for i, job in enumerate(jobs):
            name = job.get_text(strip=True)
            _id = job['id']
            referer_url = 'https://so.dajie.com/job/search?positionFunction=%s&positionName=%s' % (
                _id, name)
            yield Request(referer_url, meta={'cookiejar': i, '_id': _id}, callback=self.parse1)

    def parse1(self, response):
        _id = response.meta['_id']
        url = 'https://so.dajie.com/job/ajax/search/filter?keyword=&order=0&city=&recruitType=&salary=&experience=&page=1&positionFunction=%s&_CSRFToken=&ajax=1' % _id
        yield Request(url, meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse2)

    def parse2(self, response):
        if response.status in [403, 302]:
            ipdb.set_trace()
        headers = response.request.headers
        data = json.loads(response.text)['data']
        totalpage = data['totalPage']
        result_list = data['list']
        labels = {'compHref', 'compName', 'imgSrc', 'industryName', 'jobHref', 'jobName', 'liHref',
                  'logoHref', 'pubCity', 'pubComp', 'pubEdu', 'pubEx', 'salary', 'scaleName', 'time'}
        for item in result_list:
            info = {key: item[key] for key in item if key in labels}
            _item = DajieItem(info)
            yield _item
        for page in range(2, totalpage):
            url = re.sub(r'page=\d+', 'page=%s' % page, response.url)
            yield Request(url, meta={'cookiejar': response.meta['cookiejar']}, headers=headers, callback=self.parse2)
