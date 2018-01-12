# -*- coding: utf-8 -*-
import scrapy
import json


# 验证IP_POOL中的IP代理的有效性
# scrapy crawl ip_service
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

        ip_pool = []
        with open('E:\git\sandland\proxy_ip.jl') as f:
            for line in f:
                ip_proxy = json.loads(line)
                ip_pool.append(ip_proxy)

        for ip_proxy in ip_pool:
            proxy = '%s://%s:%s' % (ip_proxy['protocol'].lower(), ip_proxy['ip'], ip_proxy['port'])
            self.log('proxy: %s' % proxy)
            yield scrapy.Request(url, callback=self.parse, errback=self.parse_err,
                                 meta={'proxy': proxy, 'handle_httpstatus_all ': True},
                                 dont_filter=True)

    def parse_err(self, failure):
        proxy = failure.request.meta['proxy']
        self.log('proxy: %s is invalid' % proxy)

    def parse(self, response):
        src_request = response.request
        proxy = src_request.meta['proxy']
        if response.status == 200:
            self.log('proxy: %s is useful' % proxy)
        else:
            self.log('proxy: %s is invalid,status: %s' % (proxy, response.status))

