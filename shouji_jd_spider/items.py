# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ShoujiJdSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 手机编号
    id = scrapy.Field()
    # 商品标题
    title = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 型号
    type1 = scrapy.Field()
    # 入网型号
    type2 = scrapy.Field()
    # 上市时间
    time = scrapy.Field()
    # 手机颜色
    phone_color = scrapy.Field()
    # 手机壳材质
    phone_material = scrapy.Field()
    # 操作系统
    opreating_system = scrapy.Field()
    # CPU名称
    cpu_name = scrapy.Field()
    # CPU数
    core_nums = scrapy.Field()
    # SIM类型
    sim = scrapy.Field()
    # 最大支持SIM卡数量
    sim_max_nums = scrapy.Field()
    # ROM容量
    rom = scrapy.Field()
    # RAM容量
    ram = scrapy.Field()
    # 屏幕尺寸
    screen_size = scrapy.Field()
    # 分辨率
    resolution = scrapy.Field()
    # 屏幕材质
    screen_material = scrapy.Field()
    # 电池容量
    battery = scrapy.Field()
    # 商品详情页链接
    url = scrapy.Field()
    # 添加数据来源
    data_source = scrapy.Field()

