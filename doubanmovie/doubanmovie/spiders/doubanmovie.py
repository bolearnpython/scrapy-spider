from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
import ipdb
import re
from bs4 import BeautifulSoup
from ..items import DoubanmovieItem
class DouBanMovie(RedisSpider):
    name='doubanmovie'
    base_url='https://movie.douban.com'
    def start_requests(self):
        urls=['https://movie.douban.com/tag/?view=type','https://movie.douban.com/tag/?view=cloud']
        for url in urls:
            yield Request(url,dont_filter=True)
    def parse(self,response):
        bs=BeautifulSoup(response.text,'lxml')
        tags=bs('a',href=re.compile(r'/tag/\w+'),text=True)
        for tag in tags:
            yield Request(self.base_url+tag['href'],callback=self.parse1,dont_filter=True)
    def parse1(self,response):
        bs=BeautifulSoup(response.text,'lxml')
        div_movies = bs.find_all("a", class_="nbg", title=True)
        for item in div_movies:
            url=item.get('href')
            yield Request(url,meta={'url':url},callback=self.parse2)
        # 获取列表页的下一页
        next_page = bs.find("span", class_="next")
        if next_page:
            next_page_a = next_page.find("a")
            if next_page_a:
                print(0)
                yield Request(next_page_a.get("href"),callback=self.parse1,dont_filter=True)
    def parse2(self,response):
        url=response.meta['url']
        bs=BeautifulSoup(response.text,'lxml')
        content = bs.find("div", id="content")

        # 标题
        item=DoubanmovieItem()
        name_and_year = [item.get_text() for item in content.find("h1").find_all("span")]
        name, year = name_and_year if len(name_and_year) == 2 else (name_and_year[0], "")
        item['url'],item['name'],item['year'] = [url, name.strip(), year.strip("()")]

        # 左边
        content_left = bs.find("div", class_="subject clearfix")

        nbg_soup = content_left.find("a", class_="nbgnbg").find("img")
        item['img']=nbg_soup.get("src") if nbg_soup else ""

        info = content_left.find("div", id="info").get_text()
        item['movie_info'] = dict([line.strip().split(":", 1) for line in info.strip().split("\n") if line.strip().find(":") > 0])

        # 右边
        content_right = bs.find("div", class_="rating_wrap clearbox")
        if content_right:
            item['rate']=content_right.find("strong", class_="ll rating_num").get_text()

            rating_people = content_right.find("a", class_="rating_people")
            item['rate_people']=rating_people.find("span").get_text() if rating_people else ""

            item['rating_per_list'] = [item.get_text() for item in content_right.find_all("span", class_="rating_per")]
        else:
            item['rate'],item['rate_people'],item['rating_per_list']=['','','']
        yield item