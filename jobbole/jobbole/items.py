# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader
import re
import datetime
import hashlib
def newcreatdata(value):
    value=re.match('.*?(\d+).*',value,re.S)
    try:
        nums=value.group(1)
    except:
        nums=0
    return nums

def newcreatdate(value):
    value=value.replace("·","").strip()
    try:
        datetimenew=datetime.datetime.strptime(value,'%y-%m-%d').date()
    except:
        datetimenew=datetime.datetime.now().date()
    return datetimenew

def tags_date(value):
    if "评论" in value:
        return value
def md5_jm(value):
    if isinstance(value,str):
        values=value.encode('utf-8')
        m=hashlib.md5()
        m.update(values)
        return m.hexdigest()

class NewaItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class JobboleItem(scrapy.Item):

    title=scrapy.Field()
    datalist=scrapy.Field(
        input_processor=MapCompose(newcreatdate)
    )
    dianzang=scrapy.Field(
        input_processor=MapCompose(newcreatdata),
        #output_processor = TakeFirst()
    )
    shouchang=scrapy.Field(
        input_processor=MapCompose(newcreatdata)
        ,#output_processor = TakeFirst()
    )
    pinglunshu=scrapy.Field(
        input_processor=MapCompose(newcreatdata)
    )
    zhengwen=scrapy.Field()
    tag=scrapy.Field(
        input_processor=MapCompose(tags_date)
    )
    image_url_id=scrapy.Field(
        input_processor=MapCompose(md5_jm)
    )
    image_url_list=scrapy.Field()
    image_url_file = scrapy.Field()

