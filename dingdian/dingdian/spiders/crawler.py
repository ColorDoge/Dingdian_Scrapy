# -*- coding: utf-8 -*-
import scrapy
from dingdian.items import pageItem
from bs4 import BeautifulSoup
from dingdian.tools.getIp import getProxy
from dingdian.tools.getUserAgent import getUserAgent
from scrapy import Request

 


class dingdianSpider(scrapy.Spider):
    name = 'dingdian'
    allowed_domains = ['www.23us.so']
    start_urls = ['https://www.23us.so/files/article/html/13/13332/index.html']
    page_urls = []

    
    
    def start_requests(self):
        """
        这是一个重载函数，它的作用是发出第一个Request请求
        :return:
        """
        # 带着headers、cookies去请求self.start_urls[0],返回的response会被送到
        # 回调函数parse中
        
        headers = {
        'Connection': 'keep - alive',
        'User-Agent': getUserAgent()
        }
        url = self.start_urls.pop()

        yield Request(url=url, callback=self.parse, headers=headers, dont_filter=True)

    
    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        content = soup.find('div', attrs={'id': 'a_main'})
        url_ = content.find('table', attrs={'id': 'at'})
        url_list = url_.find_all('a')
        for url in url_list:
            #item = indexItem()
            #item['title'] = url.text
            #item['url'] = url.attrs['href']
            #yield
            real_url = url.attrs['href']
            self.page_urls.append(real_url)
        # print(url_list)
         
        while len(self.page_urls):
            sub_url = self.page_urls.pop()
            headers = {
            'Connection': 'keep - alive',
            'User-Agent': getUserAgent()
            }
            yield Request(url=sub_url, callback=self.sub_parse, headers=headers, dont_filter=True)
            
            
    def sub_parse(self,response):
        soup = BeautifulSoup(response.body, "lxml")
        page = soup.find('div', attrs={'id': 'a_main'})
        page = page.find_all('dd')
        title = page[0].find('h1').text
        print("正在爬取 "+title+"...")
        content = page[2]
        content = content.text
         
        item = pageItem()
         
        item['title'] = title
        item['content'] = content
         
        yield item