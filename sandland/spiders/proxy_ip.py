# -*- coding: utf-8 -*-
import scrapy


# 用来获取IP代理地址
# scrapy crawl proxy_ip -o proxy_ip.jl -L WARNNINGS
# 这里获取IP代理地址也会出现503错误,每个ip的请求次数超出限制
# producer: 将获取的代理Ip添加到redis中
# ?: 为什么要使用producer-consumer模式?
# A: 因为producer一次会拉取大量的代理Ip,而consumer一次只能验证一个代理IP的可用性
# consumer的性能没有发挥出来
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

                    yield {
                        'proxy': proxy
                    }
        next_page = response.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)