# -*- coding: utf-8 -*-
import scrapy
import random
import json
import time


# scrapy crawl email_club_auto_check_in
class EmailClubAutoCheckInSpider(scrapy.Spider):
    name = 'email_club_auto_check_in'
    allowed_domains = ['club.mail.163.com']
    start_urls = ['http://club.mail.163.com/jifen/index.do']

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'
    }

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formid='login-form',
            formdata={'email': 'shenxf_T_1000@163.com', 'password': 'shenxfT1000'},
            callback=self.after_login
        )

    def after_login(self, response):
        if "帐号或密码错误" in str(response.body):
            self.log("Login failed")
            return
        else:
            email = response.xpath('//div[@id="dvAccountLnk"]/text()').extract_first()
            if email is not None:
                self.log('%s, 登录成功' % email)

            # 自动签到
            # $("#signinstate").attr("class","btn btn-sign btn-sign-succ");
            sign_success_link = response.xpath('//a[@id="signinstate"][contains(@class, "btn btn-sign btn-sign-succ")]').extract_first()
            # response.xpath('//a[@id="signinstate"]')
            if sign_success_link is not None:
                # 已签到
                self.log('%s,已签到.' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                return

            sign_req = '../mission/task/signin.do?from=signinframe&random=%s' % random.random()
            yield scrapy.Request(url=response.urljoin(sign_req), callback=self.after_sign)

    def after_sign(self, response):
        result = json.loads(response.body)
        if result['retCode'] == '200':
            self.log('%s,签到成功.' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        elif result['retCode'] == '401':
            self.log('%s,已签到.' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            self.log('%s,签到失败.' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        time.sleep(60 * 60 * 24)
        yield response.follow(self.start_urls[0], callback=self.parse, dont_filter=True)
