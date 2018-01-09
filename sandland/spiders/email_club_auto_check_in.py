# -*- coding: utf-8 -*-
import scrapy


#
class EmailClubAutoCheckInSpider(scrapy.Spider):
    name = 'email_club_auto_check_in'
    allowed_domains = ['http://club.mail.163.com/jifen/index.do']
    start_urls = ['http://http://club.mail.163.com/jifen/index.do/']

    def parse(self, response):
        pass
