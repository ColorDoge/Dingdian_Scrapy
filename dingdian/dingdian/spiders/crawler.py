# -*- coding: utf-8 -*-
import scrapy
from dingdian.items import pageItem ,indexItem 
from bs4 import BeautifulSoup
from dingdian.tools.getUserAgent import getUserAgent
from scrapy import Request


class dingdianSpider(scrapy.Spider):
    name = 'dingdian'
    allowed_domains = ['www.23us.so']
    start_urls = ['https://www.23us.so/files/article/html/13/13332/index.html']
    page_urls = []
    
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }
    
    
    def start_requests(self):
        
        headers = {
        'Connection': 'keep - alive',
        'User-Agent': getUserAgent()
        }
        url = self.start_urls.pop()
        yield Request(url=url,callback=self.parse,headers=headers,meta=self.meta)

    
    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        content = soup.find('div', attrs={'id': 'a_main'})
        url_ = content.find('table', attrs={'id': 'at'})
        url_list = url_.find_all('a')
        title_class_info = content.find('dt')
        title_class_info = title_class_info.find_all('a')
        title = title_class_info[5].text
        self.article = title
        for url in url_list:
            #item = indexItem()
            # url.text
            #item['url'] = url.attrs['href']
            #yield
            real_url = url.attrs['href']
            self.page_urls.insert(0,real_url)
         
        while len(self.page_urls):
            sub_url = self.page_urls.pop()
            headers = {
            'Connection': 'keep - alive',
            'User-Agent': getUserAgent()
            }
            yield Request(url=sub_url,callback=self.sub_parse,headers=headers,meta=self.meta)
            
            
    def sub_parse(self,response):
        soup = BeautifulSoup(response.body, "lxml")
        page = soup.find('div', attrs={'id': 'a_main'})
   #获取本文标题
        page = page.find_all('dd')
        title = page[0].find('h1').text
         #print("正在爬取 "+title+"...")
        content = page[2]
        content = content.text
         
        item = pageItem()
        
        item['article'] = self.article
        item['title'] = title
        item['content'] = content
         
        yield item