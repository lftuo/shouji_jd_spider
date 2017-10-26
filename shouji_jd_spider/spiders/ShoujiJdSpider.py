#!/usr/bin/python
# -*- coding:utf8 -*-
# @Author : tuolifeng
# @Time : 2017-10-18 17:05:52
# @File : ShoujiJdSpider.py
# @Software : PyCharm
import json
import logging
import urlparse

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from shouji_jd_spider.items import ShoujiJdSpiderItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class shouji_jd_spider(scrapy.Spider):
    # 设置爬虫名称
    name = "jd_spider"
    # 设置爬虫运行域名
    allowed_domins = ["jd.com"]
    # 设置爬虫爬取URL
    start_urls = []
    # 173为总页数，不做爬取，直接登录https://list.jd.com/list.html?cat=9987,653,655查看总页数
    for i in range(173):
        url = 'https://list.jd.com/list.html?cat=9987,653,655&page=' + str(i+1)
        start_urls.append(url)

    '''
    解析手机的URL及id，有scrapy框架默认调用
    '''
    def parse(self, response):
        phones = response.xpath(".//*[@class='gl-item']")
        for phone in phones:
            # 解析手机详情页链接
            detail_url = phone.xpath("./div/div[@class='p-img']/a/@href").extract()[0]
            # 截取手机销售编号
            id = detail_url.split("/")[len(detail_url.split("/"))-1].split(".")[0]
            url = urlparse.urljoin('https://list.jd.com',detail_url)
            item = ShoujiJdSpiderItem(id=id,url=url)
            # 回调parse_detail函数进行详情解析
            request = scrapy.Request(url=url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request
    '''
    解析手机的详细参数：内存、尺寸、电池容量、价格、操作系统、核数等
    '''
    def parse_detail(self,response):
        item = response.meta['item']
        title = ""
        price = ""
        type1 = ""
        type2 = ""
        time = ""
        phone_color = ""
        phone_material = ""
        opreating_system = ""
        cpu_name = ""
        core_nums = ""
        sim = ""
        sim_max_nums = ""
        rom = ""
        ram = ""
        screen_size = ""
        resolution = ""
        screen_material = ""
        battery = ""

        # 解析标题
        title = response.xpath(".//div[@class='sku-name']").xpath("normalize-space(string(.))").extract()[0]
        # 解析价格
        id = item['id']
        if id != "":
            price_url = "https://p.3.cn/prices/mgets?skuIds=J_"+id
            try:
                r = requests.get(price_url)
                price = json.loads(r.text)[0]["p"]
            except Exception,e:
                logging.exception(e)

        # 国内售网页解析
        param_tables_normal = response.xpath(".//div[@class='Ptable']/*")
        # 全球售网页解析
        param_tables_global = response.xpath(".//div[@id='specifications']/table/tr")
        if len(param_tables_normal) > 0:
            for param_table in param_tables_normal:
                if len(param_table.xpath("./h3/text()")) > 0:
                    res = param_table.xpath("./h3/text()").extract()[0]
                    if res == '主体'.encode('utf-8'):
                        dts = param_table.xpath("./dl/dt")
                        for dt in dts:
                            current_dt = dt.xpath("./text()").extract()[0]
                            if current_dt == '型号'.encode('utf-8'):
                                # 中间有可能存在链接
                                if len(dt.xpath("./following-sibling::*")[0].xpath("./@class")) > 0 :
                                    type1 = dt.xpath("./following-sibling::*")[1].xpath("./text()").extract()[0]
                                else:
                                    type1 = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                            elif current_dt == '入网型号'.encode('utf-8'):
                                # 中间有可能存在链接
                                if len(dt.xpath("./following-sibling::*")[0].xpath("./@class")) > 0:
                                    type2 = dt.xpath("./following-sibling::*")[1].xpath("./text()").extract()[0]
                                else:
                                    type2 = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                            elif current_dt == '上市年份'.encode('utf-8'):
                                time += (dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]+" ")
                            elif current_dt == '上市月份'.encode('utf-8'):
                                time += dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                    elif res == '基本信息'.encode('utf-8'):
                        dts = param_table.xpath("./dl/dt")
                        for dt in dts:
                            current_dt = dt.xpath("./text()").extract()[0]
                            if current_dt == '机身颜色'.encode('utf-8'):
                                phone_color = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                            elif current_dt == '机身材质分类'.encode('utf-8'):
                                phone_material = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                    elif res == '操作系统'.encode('utf-8'):
                        dds = param_table.xpath("./dl/dd")
                        for dd in dds:
                            opreating_system += (dd.xpath("./text()").extract()[0]+" ")
                    elif res == '主芯片'.encode('utf-8'):
                        dts = param_table.xpath("./dl/dt")
                        for dt in dts:
                            current_dt = dt.xpath("./text()").extract()[0]
                            if current_dt == 'CPU品牌'.encode('utf-8'):
                                cpu_name = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                            elif current_dt == 'CPU核数'.encode('utf-8'):
                                core_nums = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                    elif res == '网络支持'.encode('utf-8'):
                        dts = param_table.xpath("./dl/dt")
                        for dt in dts:
                            current_dt = dt.xpath("./text()").extract()[0]
                            if current_dt == '双卡机类型'.encode('utf-8'):
                                sim = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                            elif current_dt == '最大支持SIM卡数量'.encode('utf-8'):
                                sim_max_nums = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                    elif res == '存储'.encode('utf-8'):
                        dts = param_table.xpath("./dl/dt")
                        for dt in dts:
                            current_dt = dt.xpath("./text()").extract()[0]
                            if current_dt == 'ROM':
                                rom = dt.xpath("./following-sibling::*")[1].xpath("./text()").extract()[0]
                            elif current_dt == 'RAM':
                                ram = dt.xpath("./following-sibling::*")[1].xpath("./text()").extract()[0]
                    elif res == '屏幕'.encode('utf-8'):
                        dts = param_table.xpath("./dl/dt")
                        for dt in dts:
                            current_dt = dt.xpath("./text()").extract()[0]
                            if current_dt == '主屏幕尺寸（英寸）'.encode('utf-8'):
                                screen_size = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                            elif current_dt == '分辨率'.encode('utf-8'):
                                resolution = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                            elif current_dt == '屏幕材质类型'.encode('utf-8'):
                                screen_material = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
                    elif res == '电池信息'.encode('utf-8'):
                        dts = param_table.xpath("./dl/dt")
                        for dt in dts:
                            current_dt = dt.xpath("./text()").extract()[0]
                            if current_dt == '电池容量（mAh）'.encode('utf-8'):
                                battery = dt.xpath("./following-sibling::*")[0].xpath("./text()").extract()[0]
        elif len(param_tables_global) > 0:
            trs = response.xpath(".//div[@id='specifications']/table/tr")
            for tr in trs:
                if len(tr.xpath("./td")) == 2:
                    name = tr.xpath("./td")[0].xpath("normalize-space(./text())").extract()[0]
                    value = tr.xpath("./td")[1].xpath("normalize-space(./text())").extract()[0]
                    #print name,value
                    if name == '型号'.encode('utf-8'):
                        type1 = value
                    elif name == '入网型号'.encode('utf-8'):
                        type2 = value
                    elif name == '上市年份'.encode('utf-8'):
                        time += (value+" ")
                    elif name == '上市月份'.encode('utf-8'):
                        time += value
                    elif name == '机身颜色'.encode('utf-8'):
                        phone_color = value
                    elif name == '机身材质分类'.encode('utf-8'):
                        phone_material = value
                    elif name == '操作系统'.encode('utf-8'):
                        opreating_system += (value+" ")
                    elif name == '操作系统版本'.encode('utf-8'):
                        opreating_system += (value + " ")
                    elif name == 'CPU品牌'.encode('utf-8'):
                        cpu_name = value
                    elif name == 'CPU核数'.encode('utf-8'):
                        core_nums = value
                    elif name == '双卡机类型'.encode('utf-8'):
                        sim = value
                    elif name == '最大支持SIM卡数量'.encode('utf-8'):
                        sim_max_nums = value
                    elif name == 'ROM':
                        rom = value
                    elif name == 'RAM':
                        ram = value
                    elif name == '主屏幕尺寸（英寸）'.encode('utf-8'):
                        screen_size = value
                    elif name == '分辨率'.encode('utf-8'):
                        resolution = value
                    elif name == '屏幕材质类型'.encode('utf-8'):
                        screen_material = value
                    elif name == '电池容量（mAh）'.encode('utf-8'):
                        battery = value

        item['title'] = title
        item['price'] = price
        item['type1'] = type1
        item['type2'] = type2
        item['time'] = time
        item['phone_color'] = phone_color
        item['phone_material'] = phone_material
        item['opreating_system'] = opreating_system
        item['cpu_name'] = cpu_name
        item['core_nums'] = core_nums
        item['sim'] = sim
        item['sim_max_nums'] = sim_max_nums
        item['rom'] = rom
        item['ram'] = ram
        item['screen_size'] = screen_size
        item['resolution'] = resolution
        item['screen_material'] = screen_material
        item['battery'] = battery
        yield item


if __name__ == '__main__':
    # 启动爬虫jd_spider
    process = CrawlerProcess(get_project_settings())
    process.crawl('jd_spider')
    process.start()