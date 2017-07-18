import scrapy 
from bs4 import BeautifulSoup
from scrapy.http import Request
from toutiao.items import ToutiaoItem
class TouTaioSpider(scrapy.Spider):
	"""docstring for TouTaioSpider"""
	name='toutiao'
	base_url='http://toutiao.com/'
	def start_requests(self):
		category = [
			'articles_news_society','articles_news_entertainment',
			'articles_movie','articles_news_tech','articles_digital',
			'articels_news_sports','articles_news_finance','articles_news_military',
			'articles_news_culture','articles_science_all'
			]
		for c in category:
			url=self.base_url+c
			yield Request(url,dont_filter=True)
			for page in range(1,500):
				url=self.base_url+c+'/p%d'%page
				yield Request(url,dont_filter=True)
	def parse(self,response):
		bs=BeautifulSoup(response.text,'lxml')
		items=bs.find('ul',{'data-node':'listBox'})('li')
		for item in items:
			tag_a=item.find('a',title=True)
			href,title=tag_a['href'],tag_a['title']
			print(href,title)
			yield Request(self.base_url[:-1]+tag_a['href'],meta={'href':href,'title':title},callback=self.parse1)
	def parse1(self,response):
		bs1=BeautifulSoup(response.text,'lxml')
		art_item=ToutiaoItem()
		art_item['title']=response.meta['title']
		art_item['href']=response.url
		try:
			art_item['articleInfo']=bs1.find('div','articleInfo').get_text(',',strip=True)
			art_item['content']=str(bs1.find('div','article-content'))
			art_item['labels']=bs1.find('ul','label-list').get_text(',',strip=True)
			art_item['is_article']=1
		except:
			art_item['is_article']=0
		yield art_item
