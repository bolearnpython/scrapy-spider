import re
from scrapy import Spider,Request
from ..items import JandanItem
class JanDan(Spider):
    name='jandan'
    start_urls=['http://jandan.net/ooxx']
    def parse(self,response):
        item = JandanItem()
        imgs= response.xpath('//img//@src').extract()#提取图片链接  
        filter_img=lambda url:re.match(r'//\w\w\d\.sinaimg\.cn',url)
        item['image_urls']=['http:'+i for i in filter(filter_img,imgs)]
        yield item  
        new_url= response.xpath('//a[@class="previous-comment-page"]//@href').extract_first()#翻页  
        if new_url:
            yield Request(new_url,callback=self.parse)  