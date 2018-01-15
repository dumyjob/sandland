# -*- coding: utf-8 -*-
import scrapy
import json
from ..redis_p import *


# 验证IP_POOL中的IP代理的有效性
# scrapy crawl ip_service
# consumer: 从redis中获取代理ip,验证可用性,加入到可用列表中
# todo: + 定时验证ip_pool中的代理的可用性的定时任务
class IpServiceSpider(scrapy.Spider):
    name = 'ip_service'
    allowed_domains = ['www.baidu.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            #禁用默认的User-Agent middleware
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'sandland.middlewares.RotateUserAgentMiddleware': 543

        },
        'ROBOTSTXT_OBEY': False,
        'RETRY_ENABLED': False,
        'HTTPERROR_ALLOW_ALL': True
    }

    def start_requests(self):
        url = 'https://www.baidu.com/'

        ip_pool = r.smembers(proxy_ip_key)
        for ip_proxy in ip_pool:
            proxy = ip_proxy['proxy']
            self.log('proxy: %s' % proxy)
            yield scrapy.Request(url, callback=self.parse, errback=self.parse_err,
                                 meta={'proxy': proxy, 'handle_httpstatus_all ': True},
                                 dont_filter=True)

    def parse_err(self, failure):
        proxy = failure.request.meta['proxy']
        self.log('proxy: %s is invalid, removed from set.' % proxy)

        r.srem(proxy_ip_key, proxy)

    def parse(self, response):
        src_request = response.request
        proxy = src_request.meta['proxy']
        if response.status == 200:
            # storage useful proxy
            self.log('proxy: %s is useful' % proxy)
            pip = r.pipeline()
            pip.sadd(ip_pool_key, proxy)
            pip.srem(proxy_ip_key, proxy)

            pip.execute()

        else:
            self.log('proxy: %s is invalid,status: %s' % (proxy, response.status))
            r.srem(proxy_ip_key, proxy)
