# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from ..items import SplashTestItem
import ipdb
# 'url'从请求网址预填充
# 'http_method'设置为'POST'为POST请求
# “body”被设置为请求POST请求正文
# 'html'：1，
# 'png'：1，
        # 'endpoint'：'render.json'，＃可选; 默认是render.json
        # 'splash_url'：'<url>'，＃可选; 覆盖SPLASH_URL
        # 'slot_policy'：scrapy_splash.SlotPolicy.PER_DOMAIN，
        # 'splash_headers'：{}，＃可选; 一个标题发送到Splash
        # 'dont_process_response'：True，＃可选，默认为False
        # 'dont_send_headers'：True，＃可选，默认为False
        # 'magic_response'：False，＃可选，默认为True
        #     # endpoint ='render.json'，＃可选; 默认是render.html
        # splash_url ='<url>'，＃可选; 覆盖SPLASH_URL
        # slot_policy = scrapy_splash.SlotPolicy.PER_DOMAIN，＃可选
class SplashSpider(Spider):
    name = 'scrapy_splash'
    start_urls = [
        'https://item.jd.com/2600240.html'
    ]

    # request需要封装成SplashRequest
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': '0.5', 'images': 0, 'render_all': 1}
                                # ,endpoint='render.json'
                                )

    def parse(self, response):

        # 本文只抓取一个京东链接，此链接为京东商品页面，价格参数是ajax生成的。会把页面渲染后的html存在html.txt
        # 如果想一直抓取可以使用CrawlSpider，或者把下面的注释去掉
        site = Selector(response)
        it_list = []
        it = SplashTestItem()
        # 京东价
        # prices = site.xpath('//span[@class="price J-p-2600240"]/text()')
        # it['price']= prices[0].extract()
        # print '京东价：'+ it['price']
        prices = site.xpath('//span[@class="p-price"]/span/text()')
        it['price'] = prices[0].extract() + prices[1].extract()
        print('京东价：' + it['price'])

        # 促　　销
        cxs = site.xpath('//div[@class="J-prom-phone-jjg"]/em/text()')
        strcx = ''
        for cx in cxs:
            strcx += str(cx.extract()) + ' '
        it['promotion'] = strcx
        print('促销:%s ' % strcx)

        # 增值业务
        value_addeds = site.xpath(
            '//ul[@class="choose-support lh"]/li/a/span/text()')
        strValueAdd = ''
        for va in value_addeds:
            strValueAdd += str(va.extract()) + ' '
        print('增值业务:%s ' % strValueAdd)
        it['value_add'] = strValueAdd

        # 重量
        quality = site.xpath('//div[@id="summary-weight"]/div[2]/text()')
        if len(quality):
            print('重量:%s ' % str(quality[0].extract()))
            it['quality'] = quality[0].extract()

        # 选择颜色
        colors = site.xpath('//div[@id="choose-attr-1"]/div[2]/div/@title')
        strcolor = ''
        for color in colors:
            strcolor += str(color.extract()) + ' '
        print('选择颜色:%s ' % strcolor)
        it['color'] = strcolor

        # 选择版本
        versions = site.xpath(
            '//div[@id="choose-attr-2"]/div[2]/div/@data-value')
        strversion = ''
        for ver in versions:
            strversion += str(ver.extract()) + ' '
        print('选择版本:%s ' % strversion)
        it['version'] = strversion

        # 购买方式
        buy_style = site.xpath('//div[@id="choose-type"]/div[2]/div/a/text()')
        print('购买方式:%s ' % str(buy_style[0].extract()))
        it['buy_style'] = buy_style[0].extract()

        # 套装
        suits = site.xpath('//div[@id="choose-suits"]/div[2]/div/a/text()')
        strsuit = ''
        for tz in suits:
            strsuit += str(tz.extract()) + ' '
        print('套装:%s ' % strsuit)
        it['suit'] = strsuit

        # 增值保障
        vaps = site.xpath('//div[@class="yb-item-cat"]/div[1]/span[1]/text()')
        strvaps = ''
        for vap in vaps:
            strvaps += str(vap.extract()) + ' '
        print('增值保障:%s ' % strvaps)
        it['value_add_protection'] = strvaps

        # 白条分期
        stagings = site.xpath(
            '//div[@class="baitiao-list J-baitiao-list"]/div[@class="item"]/a/strong/text()')
        strstaging = ''
        for st in stagings:
            ststr = str(st.extract())
            strstaging += ststr.strip() + ' '
        print('白天分期:%s ' % strstaging)
        it['staging'] = strstaging

        it_list.append(it)
        return it_list
