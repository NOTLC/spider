# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs #避免很多不必要的编码问题
import json
#其实scrapy也有封装了各种保存文件的方式，我们就以json为例
import pymysql as pymysql
from scrapy.exporters import JsonItemExporter


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

##保存到本地文件,自定义保存
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')
    def process_item(self, item, spider, ):
        #ensure_ascii=False这个如果不写的话，中文或者其他编码就会出现问题
        lines = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item #这里一定要记得返回去，因为下一个可能会用到pipeline
    def spider_closed(self):
        self.file.close()

#scrapy自带的
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('articleexport.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding = 'utf-8',ensure_ascii = False)
        self.exporter.start_exporting()
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item


###定制图片的pipeline
from scrapy.pipelines.images import ImagesPipeline
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            value['path'] = '图片的保存路劲以及名称'
            #设置那里的pipeline管道也需要设置这个文件，不再是scrapy的


#scrapy提供的MySQL数据库连接池，也就是，后面数据库的插入跟不上爬虫的速度的时候会造成的堵塞，出现了异步

from twisted.enterprise import adbapi
class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):#读取设置在settings里面的数据库连接的参数,当然，你得在settings里面设置了
        dbparms = dict(
            host = settings['MYSQL_HOST'],
        db = settings['MYSQL_DBNAME'],
        user = settings['MYSQL_USER'],
        passwd = settings['MYSQL_PAAAWDRD'],
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor,
        use_unicode = True,
        )
        #连接池,后面是一个字典的形式，所以上面需要转成字典
        dbpool = adbapi.ConnectionPool('pymysql',**dbparms)
        return cls(dbpool)#这里是传递

    #定义完上面的以后就可以来写我们的逻辑了e
    def process_item(self,item,spider):
        #使用twisted将mysql插入变成异步执行
        quey = self.dbpool.runInteraction(self.do_insert,item)
        quey.addErrback(self.handle_error,item,spider)#处理异常
    def handle_error(self,failure,item,spider):
        #处理异步的异常
        print(failure)
    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = '''
            insert into myjob(title,url,create_date) VALUE (%s ,%s ,%s)
        '''
        cursor.execute(insert_sql,(item['title'],item['url'],item['create_date']))



##mysql数据库的也可以使用django里面的orm集成来使用，有兴趣的话，可以在github搜索scrapy-djangoitem








