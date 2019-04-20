# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
from scrapy import signals
import json, codecs
from dingdian.items import pageItem

class DingdianPipeline(object):
    def process_item(self, item, spider):
        return item
        
class JsonWithUrlPipeline(object):
    def __init__(self):
        self.file = codecs.open('/Crawler/dingdian/dingdian/src/url.json', 'w', encoding='utf-8')
 
    def process_item(self, item, spider):
        #title = json.dumps("标题："+str(item['title']),ensure_ascii=False)+ "\n"
        # link = json.dumps("链接："+str(item['url']),ensure_ascii=False)+ "\n"
        #line = title + link
        self.file.write(item)
        return item
 
    def spider_closed(self, spider):
        self.file.close()
        
        
class TextPipeline(object):
    def __init__(self):
        self.file = codecs.open('/Crawler/dingdian/dingdian/src/test.txt', 'a+', encoding='utf-8')
 
    def process_item(self, item, spider):
        #title = json.dumps("标题："+str(item['title']),ensure_ascii=False)+ "\n"
        #link = json.dumps("链接："+str(item['url']),ensure_ascii=False)+ "\n"
        #line = title + link
        if isinstance(item, pageItem):
           self.file.write(str(item['title'])+"/n")
           self.file.write(str(item['content']))
        pass
 
    def spider_closed(self, spider):
        self.file.close()