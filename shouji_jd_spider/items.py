# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ShoujiJdSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    type1 = scrapy.Field()
    type2 = scrapy.Field()
    time = scrapy.Field()
    phone_color = scrapy.Field()
    phone_material = scrapy.Field()
    opreating_system = scrapy.Field()
    cpu_name = scrapy.Field()
    core_nums = scrapy.Field()
    sim = scrapy.Field()
    sim_max_nums = scrapy.Field()
    rom = scrapy.Field()
    ram = scrapy.Field()
    screen_size = scrapy.Field()
    resolution = scrapy.Field()
    screen_material = scrapy.Field()
    battery = scrapy.Field()
    url = scrapy.Field()

