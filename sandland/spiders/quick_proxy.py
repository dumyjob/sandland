# -*- coding: utf-8 -*-
import scrapy


# todo: 快代理spider
class QuickProxySpider(scrapy.Spider):
    name = 'quick_proxy'
    allowed_domains = ['www.kuaidaili.com']
    start_urls = ['http://www.kuaidaili.com/']

    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'ITEM_PIPELINES': {
            'sandland.pipelines.ProxyIpPipeline': 1
        },
        'DOWNLOADER_MIDDLEWARES': {
            #禁用默认的User-Agent middleware
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'sandland.middlewares.RotateUserAgentMiddleware': 543

        }
    }

    def parse(self, response):
        pass
