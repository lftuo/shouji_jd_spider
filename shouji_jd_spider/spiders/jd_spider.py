#!/usr/bin/python
# -*- coding:utf8 -*-
# @Author : tuolifeng
# @Time : 2017-10-18 17:05:52
# @File : jd_spider.py
# @Software : PyCharm
import urlparse

import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from shouji_jd_spider.items import ShoujiJdSpiderItem


class Shouji_jd_Spider(scrapy.Spider):
    name = "shouji_jd_spider"
    allowed_domins = ["jd.com"]
    start_urls = ["https://list.jd.com/list.html?cat=9987,653,655&page=1"]

    def parse(self, response):
        phones = response.xpath(".//*[@class='gl-item']")
        for phone in phones:
            #try:
            url = phone.xpath(".//*[@class='p-img']/a/@href").extract()[0]
            item = ShoujiJdSpiderItem(url=url)
            url = urlparse.urljoin('https://list.jd.com',url)
            request = scrapy.Request(url=url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request
            #except Exception,e:
            #    print e.message

    def parse_detail(self,response):
        item = response.meta['item']
        details = response.xpath(".//*[@class='itemInfo-wrap']")
        for detail in details:
            item['title'] = detail.xpath(".//*[@class='sku-name']/@text()").extract()[0]
        yield item


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('shouji_jd_spider')
    process.start()