# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShoujiJdSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()  # 商品链接
    #ID = scrapy.Field()  # 商品ID
    #name = scrapy.Field()  # 商品名字
    #model = scrapy.Field()
    #price = scrapy.Field()
    #time = scrapy.Field()
    #ranking = scrapy.Field()
    #url = scrapy.Field()
