# -*- coding: utf-8 -*-
import scrapy
import json
import time
from ..redis_p import *


# 验证IP_POOL中的IP代理的有效性
# scrapy crawl ip_service
# consumer: 从redis中获取代理ip,验证可用性,加入到可用列表中
# 能够获得的有效ip比例: ?/25686 = ?
# todo: + 定时验证ip_pool中的代理的可用性的定时任务
# todo: + 如何提高验证ip_pool的速度,现在并发速度太慢了
# 添加log信息: 1. 每个request - response/failure的时间
# 2. 有多少个request并发
# 3.
# 如何处理spider中断,已经取出来,但是还没处理完的数据如何保留?
class IpServiceSpider(scrapy.Spider):
    name = 'ip_service'
    allowed_domains = ['www.baidu.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            #禁用默认的User-Agent middleware
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'sandland.middlewares.RotateUserAgentMiddleware': 543

        },
        # 'EXTENSIONS': {
        #    'sandland.extensions.LogTimeExtension': 500
        # },
        'ROBOTSTXT_OBEY': False,
        'RETRY_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 10
    }

    def start_requests(self):
        url = 'https://www.baidu.com/'

        # todo 这里不要一下取出来,数据结构最好采用redis队列
        while True:
            ip_proxies = r.brpop(proxy_ip_queue, 100)
            if ip_proxies is not None:
                ip_proxy = ip_proxies[1]
                proxy = json.loads(str(ip_proxy, encoding='utf-8'))['proxy']
                self.log('proxy: %s' % proxy)
                yield scrapy.Request(url, callback=self.parse, errback=self.parse_err,
                                     meta={'proxy': proxy,
                                           'start_time': time.time()
                                           },
                                     dont_filter=True)

    def parse_err(self, failure):
        # self.log(failure)
        proxy = failure.request.meta['proxy']
        time_elapsed = time.time() - failure.request.meta['start_time']

        self.log('proxy: %s is invalid, removed from list. time_elapsed: %0.2f' % (proxy, time_elapsed))

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