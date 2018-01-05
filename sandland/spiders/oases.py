# -*- coding: utf-8 -*-
import scrapy


class OasesSpider(scrapy.Spider):
    name = 'oases'
    allowed_domains = ['1111avtt.com']
    start_urls = ['http://1111avtt.com/']

    def parse(self, response):

        # 爬全站链接,找到有ed2k的页面,就表示有可以下载的东西,保存
        response.re('ed2k:')

        for href in response.css('a::attr(href)'):
            yield response.follow(href, callback=self.parse)
