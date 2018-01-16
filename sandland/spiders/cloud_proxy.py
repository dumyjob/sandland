# -*- coding: utf-8 -*-
import scrapy


class CloudProxySpider(scrapy.Spider):
    name = 'cloud_proxy'
    allowed_domains = ['//www.ip3366.net']
    start_urls = ['http://www.ip3366.net/']

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
