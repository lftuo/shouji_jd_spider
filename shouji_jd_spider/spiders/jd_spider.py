#!/usr/bin/python
# -*- coding:utf8 -*-
# @Author : tuolifeng
# @Time : 2017-10-18 17:05:52
# @File : jd_spider.py
# @Software : PyCharm
import urlparse

import scrapy
from requests import Response
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from bs4 import BeautifulSoup
from shouji_jd_spider.items import ShoujiJdSpiderItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Shouji_jd_Spider(scrapy.Spider):
    name = "shouji_jd_spider"
    allowed_domins = ["jd.com"]
    #start_urls = ["https://list.jd.com/list.html?cat=9987,653,655"]
    start_urls = []
    for i in range(1):
        url = 'https://list.jd.com/list.html?cat=9987,653,655&page=' + str(i)
        start_urls.append(url)

    def parse(self, response):
        phones = response.xpath(".//*[@class='gl-item']")
        for phone in phones:
            #try:
            #print phone.xpath("/@data-sku")
            url = phone.xpath("./div/div[@class='p-img']/a/@href").extract()[0]
            price = phone.xpath("./div/div[@class='p-price']/strong[@class='J_price']/*")
            print price
            item = ShoujiJdSpiderItem(url=url)
            url = urlparse.urljoin('https://list.jd.com',url)
            request = scrapy.Request(url=url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request
            #except Exception,e:
            #    print e.message
        # 解析下一页
        #next_page = Selector(response).re(u'<a class="pn-next" href=".*">下一页<i>&gt;</i></a>')
        #if next_page:
        #    print next_page[0]
        #    yield scrapy.Request(url=next_page[0],callback=self.parse)

    def parse_detail(self,response):
        Selector(response)
        item = response.meta['item']
        details = response.xpath(".//*[@class='itemInfo-wrap']/*")
        print '-------------------------------------'
        for detail in details:
            if detail.re(r"<div class=\"sku-name\">"):
                #print detail.xpath("normalize-space(string(.))").extract()[0]
                # 解析标题
                item['title'] = detail.xpath("normalize-space(string(.))").extract()[0]
            if detail.re(r"<div class=\"summary summary-first\">"):
                item['ID'] = detail.xpath("./div/div/div[@class='dd']/a/@data-sku").extract()[0]
                id = str(detail.xpath("./div/div/div[@class='dd']/a/@data-sku").extract()[0])
                class_=('price J-p-%s'%id)
                price = detail.xpath("./div/div/div[@class='dd']/span[@class='p-price']/span[@class='price J-p-%s']/@text"%id)
                print price
                #print class_
                #spans  = detail.xpath("./div/div/div[@class='dd']/span/*")
                #for span in spans:
                #    if span.re(r"<span class=\"price J-p-%s\">"%id):
                #        print span
                #        print span.xpath("./@text")
        yield item


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('shouji_jd_spider')
    process.start()