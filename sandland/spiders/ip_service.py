# -*- coding: utf-8 -*-
import scrapy
import json
from ..redis_p import *


# 验证IP_POOL中的IP代理的有效性
# scrapy crawl ip_service
# consumer: 从redis中获取代理ip,验证可用性,加入到可用列表中
# 能够获得的有效ip比例: ?/25686 = ?
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

        # todo 这里不要一下取出来,数据结构最好采用redis队列
        while True:
            ip_proxy = r.brpop(proxy_ip_queue, 100)
            if ip_proxy is not None:
                proxy = json.loads(str(ip_proxy, encoding='utf-8'))['proxy']
                self.log('proxy: %s' % proxy)
                yield scrapy.Request(url, callback=self.parse, errback=self.parse_err,
                                     meta={'proxy': proxy, 'handle_httpstatus_all ': True},
                                     dont_filter=True)

    def parse_err(self, failure):
        proxy = failure.request.meta['proxy']
        self.log('proxy: %s is invalid, removed from list.' % proxy)

    def parse(self, response):
        src_request = response.request
        proxy = src_request.meta['proxy']
        if response.status == 200:
            # storage useful proxy
            self.log('proxy: %s is useful' % proxy)
            r.sadd(ip_pool_key, str(proxy))

        else:
            self.log('proxy: %s is invalid,status: %s' % (proxy, response.status))


# def main():
#     s = '{"proxy": "https://123.185.129.189:8080"}'
#
#     json.loads(s)
#
# if __name__ == '__main__':
#     main()