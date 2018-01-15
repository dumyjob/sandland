# -*- coding: utf-8 -*-
import scrapy


# 用来获取IP代理地址
# scrapy crawl proxy_ip -o proxy_ip.jl -L WARNNINGS
# 这里获取IP代理地址也会出现503错误,每个ip的请求次数超出限制
class ProxyIpSpider(scrapy.Spider):
    name = 'proxy_ip'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/']

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'ITEM_PIPELINES': {
            'sandland.pipelines.ProxyIpPipeline': 1
        },
        'DOWNLOADER_MIDDLEWARES': {
            #禁用默认的User-Agent middleware
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'sandland.middlewares.RotateUserAgentMiddleware': 543

        },
        'ROBOTSTXT_OBEY': False,
        'RETRY_ENABLED': False,
        'HTTPERROR_ALLOW_ALL': True
    }

    # 代理IP可用性验证url
    url = 'https://www.baidu.com/'

    # 爬取代理网站上提供的代理IP
    def parse(self, response):
        ip_proxies = response.xpath('//table[@id="ip_list"]/tr')

        if ip_proxies:
            for ip_proxy in ip_proxies:
                ip = ip_proxy.xpath('td[2]/text()').re(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}')
                port = ip_proxy.xpath('td[3]/text()').re(r'\d{1,5}')
                protocol = ip_proxy.xpath('td[6]/text()').extract_first()

                if ip:
                    ip = ip[0]
                    port = port[0]
                    proxy = '%s://%s:%s' % (protocol.lower(), ip, port)
                    self.log('proxy: %s' % proxy)
                    # todo: 这里request应该不需要遵循反爬规则,频率太低验证不过来
                    yield scrapy.Request(self.url, callback=self.parse_success, errback=self.parse_err,
                                         meta={'proxy': proxy, 'handle_httpstatus_all ': True},
                                         dont_filter=True)

        next_page = response.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    # 代理IP验证失败,记Log
    def parse_err(self, failure):
        proxy = failure.request.meta['proxy']
        self.log('proxy: %s is invalid' % proxy)

    # 代理IP验证成功
    def parse_success(self, response):
        src_request = response.request
        proxy = src_request.meta['proxy']
        if response.status == 200:
            self.log('proxy: %s is useful' % proxy)
            yield {
                'proxy': proxy
            }
        else:
            self.log('proxy: %s is invalid,status: %s' % (proxy, response.status))
