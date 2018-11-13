from scrapy_redis.spiders import RedisSpider
from urllib import parse
from scrapy.loader import ItemLoader
import scrapy
from scrapy import Request
import re
from jobberder.items import JobboleItem
import datetime
import scrapy_redis.scheduler
class JobberSpider(RedisSpider):
    name = 'jobber'
    allowed_domains = ['blog.jobbole.com']
    redis_key = 'jobber:start_urls'

    def parse(self, response):
        pones = response.css("#archive .floated-thumb .post-thumb a")
        # for poness in pones:
        #     pors_urls = poness.css('::attr(href)').extract_first()
        #     image_url = poness.css('img::attr(src)').extract_first()
        yield Request( 'http://blog.jobbole.com/114407/',callback=self.parse_detail)


    def parse_detail(self, response):
         pass
    #     # 内置loader方法
    #     item = JobboleItem()
    #     image_url = response.meta.get("image_url_list", "")
    #     item_loader = ItemLoader(item=JobboleItem(), response=response)
    #     item_loader.add_xpath("title", "//div[@class='entry-header']/h1/text()")
    #     item_loader.add_css("datalist", ".entry-meta p::text")
    #     item_loader.add_css("dianzang", ".vote-post-up h10::text")
    #     item_loader.add_css("shouchang", ".bookmark-btn ::text")
    #     item_loader.add_css("pinglunshu", "a .href-style ::text")
    #     item_loader.add_css("tag", ".entry-meta-hide-on-mobile a ::text")
    #     item_loader.add_value("image_url_id", image_url)
    #     item_loader.add_value("image_url_list", image_url)
    #
    #     item = item_loader.load_item()
    #     yield item