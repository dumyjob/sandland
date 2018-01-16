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

        proxies = response.xpath('//*[@id="list"]/table/tbody/tr')
        # response.xpath('//*[@id="list"]/table/tbody/tr/td[4]/text()')
        if proxies:
            for proxy in proxies:
                ip = proxy.xpath('td[1]/text()').extract_first()
                port = proxy.xpath('td[2]/text()').extract_first()
                protocol = proxy.xpath('td[4]/text()').extract_first().lower()

                yield {
                    'proxy': '%s://%s:%s' % (protocol, ip, port)
                }

        next_page = response.xpath('//').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

