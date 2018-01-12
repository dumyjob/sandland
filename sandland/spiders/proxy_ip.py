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
        'DOWNLOAD_DELAY': 3
    }

    def parse(self, response):
        ip_proxies = response.xpath('//table[@id="ip_list"]/tr')

        if ip_proxies:
            for ip_proxy in ip_proxies:
                ip = ip_proxy.xpath('td[2]/text()').re(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}')
                port = ip_proxy.xpath('td[3]/text()').re(r'\d{1,5}')
                protocol = ip_proxy.xpath('td[6]/text()').extract_first()

                if ip:
                    yield {
                        'ip': ip[0],
                        'port': port[0],
                        'protocol': protocol
                    }

        next_page = response.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

