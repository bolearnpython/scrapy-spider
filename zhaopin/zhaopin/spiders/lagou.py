
import re
import ipdb
import logging
import json
from bs4 import BeautifulSoup
from ..items import LagouItem
from scrapy import FormRequest, Spider


class LaGou(Spider):
    name = 'lagou'
    start_urls = ['https://www.lagou.com']

    def parse(self, response):
        bs = BeautifulSoup(response.text, 'lxml')
        jobs = [a.text for a in bs.find('div', 'mainNavs').find_all('a')]
        for kd in jobs:
            data = {'first': 'false', 'pn': '1', 'kd': kd}
            url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
            yield FormRequest(url=url, formdata=data, meta={'data': data, 'city': '全国'}, callback=self.parse1)
            for city in {'上海', '深圳', '广州', '杭州', '成都', '重庆', '大连', '南京', '武汉', '西安', '厦门', '长沙', '苏州', '天津'}:
                url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%s&needAddtionalResult=false' % city
                yield FormRequest(url=url, formdata=data, meta={'data': data, 'city': city}, callback=self.parse1)

    def parse1(self, response):
        data = response.meta['data']
        city = response.meta['city']
        result = json.loads(response.text)['content'][
            'positionResult']['result']
        labels = {'city', 'positionId', 'companyFullName', 'companyLabelList', 'companyLogo', 'companyShortName', 'companySize', 'createTime',
                  'education', 'financeStage', 'firstType', 'industryField', 'jobNature', 'positionAdvantage', 'positionName', 'salary', 'secondType', 'workYear'}
        for item in result:
            info = {key: item[key] for key in item if key in labels}
            _item = LagouItem(info)
            yield _item
        if len(result) == 15:
            if data['pn'] != '30':
                data['pn'] = str(int(data['pn']) + 1)
                yield FormRequest(url=response.url, formdata=data, meta={'data': data, 'city': city}, callback=self.parse1)
