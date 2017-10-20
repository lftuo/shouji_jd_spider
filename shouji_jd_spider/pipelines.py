# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from scrapy.exceptions import DropItem


class ShoujiJdSpiderPipeline(object):

    def __init__(self):
        self.file = open('shouji_jd.json','wb')

    def process_item(self, item, spider):
        #if item['link']:
        line = json.dumps(dict(item),ensure_ascii=False).decode('utf8') + "\n"
        self.file.write(line)
        return item
        #else:
            #raise DropItem("Missing title in %s" % item)

