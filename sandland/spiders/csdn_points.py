# -*- coding: utf-8 -*-
import scrapy


class CsdnPointsSpider(scrapy.Spider):
    name = 'csdn_points'
    allowed_domains = ['https://www.csdn.net/']
    start_urls = ['http://https://www.csdn.net//']

    def parse(self, response):
        pass
