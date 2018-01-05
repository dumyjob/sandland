# -*- coding: utf-8 -*-
import scrapy


# 双色球爬虫
# scrapy crawl union_lotto -o union_lotto.jl
class UnionLottoSpider(scrapy.Spider):
    name = 'union_lotto'
    allowed_domains = ['http://www.cwl.gov.cn/']
    start_urls = ['http://www.cwl.gov.cn/kjxx/ssq/hmhz/index.shtml']

    def parse(self, response):
        rows = response.xpath('//div[@class="page_box clearself mt10"]/table[1]/tbody/tr')
        for row in rows:
            # 不是数据项的skip
            if row.xpath('td[1]/text()').re(r'\d{7}'):
                yield {
                    'serial': row.xpath('td[1]/text()').extract_first(),
                    'red_nos': row.xpath('td[2]/p/span/text()').extract(),
                    'blue_no': row.xpath('td[3]/p/span/text()').extract_first().strip(),
                    'first_num': row.xpath('td[4]/text()').extract_first(),
                    'sale_amt': row.xpath('td[5]/text()').extract_first(),
                    'pool_amt': row.xpath('td[6]/text()').extract_first()
                }

                link_detail = row.xpath('td[7]/a/@href').extract_first()
                yield response.follow(link_detail, self.parse_detail, dont_filter=True)

        # 分页搜索
        next_or_pre_pages = response.xpath('//div[@class="pagebar"]/table/tr/td/a/span[@class="fc_ch1"]/../@href')
        end = response.xpath('//div[@class="pagebar"]/table/tr/td/span[@class="fc_hui2"]/text()').extract_first()
        # 没有到最后一页,到了最后一页,就不再继续搜索了
        if end is None or '下一页' != end and next_or_pre_pages is not None:
            next_page = next_or_pre_pages[1] if len(next_or_pre_pages) > 1 else next_or_pre_pages[0]
            yield response.follow(next_page, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        detail_info = response.xpath('//div[@class="page_box clearself mt10"]/div[@class="drawright"]')

        info = detail_info.xpath('ul/li[@class="caizhong"]')
        no = detail_info.xpath('ul/li[@class="haoma3"]/span/text').extract()
        wins = []
        for win_info in detail_info.xpath('table/tbody/tr'):
            win = {
                'level': win_info.xpath('td[1]/text()').extract_first(),
                'num': win_info.xpath('td[2]/text()').extract_first(),
                'amt': win_info.xpath('td[3]/text()').extract_first()
            }
            wins.append(win)
        win_first = detail_info.xpath('div[@class="mt10"]/text()').extract_first().strip()

        yield {
            'serial': info.xpath('span[1]/text()').re(r'\d{7}')[0],
            'date': info.xpath('span[2]/text()').re(r'\d{4}-\d{2}-\d{2}')[0],
            'sale_amt': info.xpath('span[3]/i/text()').extract_first(),
            'pool_amt': info.xpath('span[4]/i/text()').extract_first(),
            'no': no,
            'wins': wins,
            'win_first': win_first
        }
