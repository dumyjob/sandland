# -*- coding: utf-8 -*-
import scrapy


# todo: 快代理spider
class QuickProxySpider(scrapy.Spider):
    name = 'quick_proxy'
    allowed_domains = ['www.kuaidaili.com']
    start_urls = ['https://www.kuaidaili.com/free/']

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
        if proxies:
            for proxy in proxies:
                ip = proxy.xpath('td[1]/text()').extract_first()
                port = proxy.xpath('td[2]/text()').extract_first()
                protocol = proxy.xpath('td[4]/text()').extract_first().lower()

                yield {
                    'proxy': '%s://%s:%s' % (protocol, ip, port)
                }

        next_page = response.xpath('//*[@id="listnav"]/ul/li/a[@class="active"]/../following-sibling::li[1]/a/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)