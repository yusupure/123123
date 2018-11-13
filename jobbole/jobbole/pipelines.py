# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from  scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
import pymysql
from twisted.enterprise import adbapi
import MySQLdb.cursors
#import
from modls.es_save import ArticleType


class JobbolePipeline(object):
    def process_item(self, item, spider):
        return item
#自定义JSON导出方法tag,title,
class JsonLoaderPipeline(object):
    def __init__(self):
        self.file=codecs.open("text.json",'w',encoding='utf-8')

    def process_item(self, item, spider):
        jsonlist=json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(jsonlist)
        return item
    def close_json(self,spider):
        self.file.close()

#scrapy自带导出JSON功能
class JsonItemPipeline(object):
    def __init__(self):
        self.file=open('text2.json','wb')
        self.expor=JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.expor.start_exporting()
    def close_spider(self,spider):
        self.expor.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.expor.export_item(item)
        return item

#scrapy下载图片方式
class ImageloaderPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            iamge_value=value['path']
            item['image_url_file']=iamge_value
            return item

#自定时MYsql导入数据
# class MysqldownsPipeline(object):
#     def __init__(self):
#         self.db=pymysql.connect(host='127.0.0.1',port=3339,user='root',password='root',db='test',charset='utf8')
#         self.cur=self.db.cursor()
#
#     def process_item(self, item, spider):
#         insert_sql='''
#               insert into jobble (image_url_id,image_url_list,image_url_file,tag,title) VALUES (%s,%s,%s,%s,%s)
#         '''
#         sql_data=item["image_url_id"],item["image_url_list"],item["image_url_file"],item["tag"],item["title"]
#         self.cur.execute(insert_sql,sql_data)
#         self.db.commit()
#         return item

#内置SCRAPY SQL方法
class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool
    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            port=settings["MYSQL_PORT"],
            charset = "utf8",
            use_unicode = True,
            cursorclass = MySQLdb.cursors.DictCursor,
        )
        dbpool=adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = '''
                      insert into jobble (image_url_id) VALUES (%s,%s,%s)
                '''
        #sql_data =
        cursor.execute(insert_sql, item["image_url_id"])


class ElasicsearchPipline(object):
    def process_item(self, item, spider):
        article=ArticleType()

        article.title =item['title']
        article.datalist =item['datalist']
        article.dianzang =item['dianzang']
        article.shouchang =item['shouchang']
        article.pinglunshu =item['pinglunshu']
        #article.zhengwen =item['zhengwen']
        #article.tag = item['tag']
        article.save()
        return item
