# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging

from MySQLdb.cursors import DictCursor
from twisted.enterprise import adbapi


class ShoujiJdSpiderPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    def _conditional_insert(self, tx, item):
        sql = "insert into shouji_jd_spider_data(id,title,price,type1,type2,model,time,phone_color,phone_material,opreating_system,cpu_name,core_nums,sim,sim_max_nums,rom,ram,screen_size,resolution,screen_material,battery,url,data_source) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            params = (item["id"],item["title"],item["price"],item["type1"],item["type2"],item["model"],item["time"],item["phone_color"],item["phone_material"],item["opreating_system"],item["cpu_name"],item["core_nums"],item["sim"],item["sim_max_nums"],item["rom"],item["ram"],item["screen_size"],item["resolution"],item["screen_material"],item["battery"],item["url"],item["data_source"])
            tx.execute(sql, params)
        except Exception,e:
            logging.exception(e)
            print "ERROR HERE ----",item['url']


    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue

