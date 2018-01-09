# -*- coding: utf-8 -*-
import scrapy


# zoho email reg spider: zoho邮箱注册
class ZohoEmailRegSpider(scrapy.Spider):
    name = 'zoho_email_reg'
    allowed_domains = ['http://https://mail.zoho.com.cn/signup.do/']
    start_urls = ['http://http://https://mail.zoho.com.cn/signup.do//']

    def parse(self, response):
        pass
