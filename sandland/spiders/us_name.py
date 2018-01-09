# -*- coding: utf-8 -*-
import scrapy


# US'person name spider: 获取外国人的英文名,在一些注册中会使用到
# 如何让爬虫爬取到一定数据,就暂停; 在暂停之后,如果有需要,怎么重新启动爬虫,但是有不会重新爬取数据
# 主要目标网站: stackoverflow / facebook / yahoo ...
# 具体参考: https://www.zhihu.com/question/20247711
class UsNameSpider(scrapy.Spider):
    name = 'us_name'
    allowed_domains = ['https://www.facebook.com/facebook']
    start_urls = ['http://https://www.facebook.com/facebook/']

    def parse(self, response):
        pass
