# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    #author = scrapy.Field()
    #class_ = scrapy.Field()
    #static = scrapy.Field()
    url = scrapy.Field()
    
    pass
    
    
class indexItem(scrapy.Item):
    title = scrapy.Field()

class pageItem(scrapy.Item):
    article = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()