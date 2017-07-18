# -*- coding: utf-8 -*-
# from scrapy_redis.spiders import RedisSpider
from Zhihu.items import ZhihuItem
from bs4 import BeautifulSoup
from scrapy import Request, Spider
import json
from copy import deepcopy
import ipdb


def filter_dict(old_dict, new_dict):
    for i in old_dict.keys() & new_dict.keys():
        if isinstance(old_dict[i], (str, int)):
            new_dict[i] = old_dict[i]
        elif isinstance(old_dict[i], list):
            for k, v in enumerate(old_dict[i]):
                if len(new_dict[i]) < k + 1:
                    new_dict[i].append(deepcopy(new_dict[i][0]))
                filter_dict(v, new_dict[i][k])
        else:
            filter_dict(old_dict[i], new_dict[i])


class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']

    def start_requests(self):
        _id = 'chen-yi-63-39'
        url = 'https://www.zhihu.com/people/{_id}/following'.format(_id=_id)
        headers = {'Referer': url,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36', }
        yield Request(url, meta={'_id': _id, 'Referer': url})

    def parse(self, response):
        # ipdb.set_trace()
        _id = response.meta['_id']
        bs = BeautifulSoup(response.text, 'lxml')
        data = json.loads(bs.find('div', id='data').attrs[
                          'data-state'])['entities']['users']
        info = data[_id]
        info['description'] = BeautifulSoup(info['description'], 'lxml').text
        educations = {'major': {'name': ''}, 'school': {'name': ''}}
        employments = {'company': {'name': ''}, 'job': {'name': ''}}
        locations = {'name': ''}
        # 关注了
        count1 = {'followingCount', 'followerCount'}
        count2 = {'answerCount', 'questionCount', 'columnsCount', 'favoriteCount', 'articlesCount', 'participatedLiveCount',
                  'followingColumnsCount', 'followingTopicCount', 'followingQuestionCount', 'followingFavlistsCount'}
        # 赞同,感谢,收藏,公共编辑
        count3 = {'voteupCount', 'favoritedCount', 'thankedCount', 'logsCount'}
        count = {i: ''for i in count1 | count2 | count3}
        info_ = {**count, 'description': '', 'educations': [educations], 'employments': [
            employments], 'business': {'name': ''}, 'locations': [locations], 'headline': '', 'name': ''}
        filter_dict(info, info_)
        yield ZhihuItem(info_)
        for id in data:
            referer_url = 'https://www.zhihu.com/people/{id}/'.format(
                id=id)
            url = 'https://www.zhihu.com/people/{id}/following'.format(
                id=id)
            yield Request(url, meta={'_id': id, 'Referer': referer_url})
