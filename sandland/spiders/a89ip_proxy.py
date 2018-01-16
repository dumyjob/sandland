# -*- coding: utf-8 -*-
import scrapy


# 89ip代理spider
class A89ipProxySpider(scrapy.Spider):
    name = '89ip_proxy'
    allowed_domains = ['www.89ip.cn/']
    start_urls = ['http://www.89ip.cn/']

    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'ITEM_PIPELINES': {
            'sandland.pipelines.ProxyIpPipeline': 1
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 禁用默认的User-Agent middleware
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'sandland.middlewares.RotateUserAgentMiddleware': 543

        }
    }

    def parse(self, response):
        pass

# http://www.89ip.cn/tiqv.php?sxb=&tqsl=30&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1
# Request Method:GET



