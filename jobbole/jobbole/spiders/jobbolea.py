# -*- coding: utf-8 -*-
from urllib import parse
from scrapy.loader import ItemLoader
import scrapy
from scrapy import Request
import re

from jobbole.MD5new import md5_JM
from jobbole.items import JobboleItem, NewaItemLoader
import datetime

class JobboleaSpider(scrapy.Spider):
    name = 'jobbolea'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        pones=response.css("#archive .floated-thumb .post-thumb a")
        for poness in pones:
            pors_urls=poness.css('::attr(href)').extract_first()
            image_url=poness.css('img::attr(src)').extract_first()
            yield Request(pors_urls, meta={"image_url_list":image_url},callback=self.parse_detail)
        #next_page=response.css("#archive .page-numbers ::attr('href')").extract_first()
        #yield Request(next_page,callback=self.parse)
    def parse_detail(self,response):

        # title=response.xpath("//div[@class='entry-header']/h1/text()").extract()
        # datalist=response.css('.entry-meta p::text').extract()[0].strip().replace("·","").strip()
        #
        # dianzang=response.css('.vote-post-up h10::text').extract()[0]
        # dianzang = re.match(r'.*?(\d+).*', dianzang, re.S)
        # if dianzang:
        #     dianzang=int(dianzang.group(1))
        # else:
        #     dianzang=0
        #
        # shouchang=response.css('.bookmark-btn ::text').extract()[0]
        # shouchang = re.match(r'.*?(\d+).*', shouchang, re.S)
        # if shouchang:
        #     shouchang=int(shouchang.group(1))
        # else:
        #     shouchang=0
        #
        # pinglunshu = response.css('a .href-style ::text').extract()[0]
        # pinglunshu = re.match(r'.*?(\d+).*', pinglunshu, re.S)
        # if pinglunshu:
        #     pinglunshu=int(pinglunshu.group(1))
        # else:
        #     pinglunshu=0
        #
        # zhengwen=response.css('.entry').extract()[0]
        #
        # biaoqian = response.css('.entry-meta-hide-on-mobile a ::text').extract()
        # biaoqian=[biaoqiannew for biaoqiannew in biaoqian if not biaoqiannew.strip().endswith("评论")]
        # tag = ",".join(biaoqian)
        #

        #
        # item["title"]=title
        # try:
        #     datetime.datetime.strptime("datalist","%y/%m/%d").date()
        # except:
        #     datetime.datetime.now().date()
        # item["datalist"]=datalist
        # item["dianzang"]=dianzang
        # item["shouchang"]=shouchang
        # item["pinglunshu"]=pinglunshu
        # #item["zhengwen"]=zhengwen
        # item["tag"]=tag
        # item["image_url_id"]=md5_JM(image_url)
        # item["image_url_list"]=[image_url]

        #内置loader方法
        item = JobboleItem()
        image_url = response.meta.get("image_url_list", "")
        item_loader=NewaItemLoader(item=JobboleItem(),response=response)
        item_loader.add_xpath("title","//div[@class='entry-header']/h1/text()")
        item_loader.add_css("datalist",".entry-meta p::text")
        item_loader.add_css("dianzang", ".vote-post-up h10::text")
        item_loader.add_css("shouchang", ".bookmark-btn ::text")
        item_loader.add_css("pinglunshu", "a .href-style ::text")
        item_loader.add_css("tag", ".entry-meta-hide-on-mobile a ::text")
        item_loader.add_value("image_url_id",image_url)
        item_loader.add_value("image_url_list", image_url)

        item=item_loader.load_item()
        yield item
