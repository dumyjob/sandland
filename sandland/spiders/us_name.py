# -*- coding: utf-8 -*-
import scrapy


# US'person name spider: 获取外国人的英文名,在一些注册中会使用到
# 如何让爬虫爬取到一定数据,就暂停; 在暂停之后,如果有需要,怎么重新启动爬虫,但是有不会重新爬取数据
# 主要目标网站: stackoverflow / facebook / yahoo ...
# 具体参考: https://www.zhihu.com/question/20247711
# GitHub:
# StackOverflow:
# Quora:
# Facebook:
# Twitter:
# Youtube:
# scrapy crawl us_name -o us_name.jl
# 持久化:
# todo q: 出现response.status = 429 too many Request: 采用IP池/代理; sleep一会
class UsNameSpider(scrapy.Spider):
    name = 'us_name'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/tags/']

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'ITEM_PIPELINES': {
             'sandland.pipelines.UsNamePipeline': 1
        },
        'DOWNLOADER_MIDDLEWARES': {
            #禁用默认的User-Agent middleware
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'sandland.middlewares.RotateUserAgentMiddleware': 543,
            'sandland.middlewares.IpProxyMiddleware': 544
        }
    }

    def parse(self, response):
        tags = response.xpath('//div[@id="tags_list"]/table[@id="tags-browser"]/tr/td[@class="tag-cell"]')
        # response.xpath('//div[@id="tags_list"]')
        # /table[@id="tags-browser"]/tr/td[@class="tag-cell"
        # tag_list
        self.log('总共: %s tag' % len(tags))
        for tag_href in tags.xpath('a/@href').extract():
            if tag_href is not None:
                yield response.follow(tag_href, callback=self.parse_tag)

        # next tag page: tag_list
        next_page = response.xpath('//div[@class="pager fr"]/a[@rel="next"]/@href').extract_first()
        if next_page is not None and next_page.strip() != '':
            self.log('下一页 tag')
            yield response.follow(next_page, callback=self.parse)

    # 每个tag下的questions列表
    def parse_tag(self, response):
        questions = response.xpath('//div[@id="questions"]/div[@class="question-summary"]')

        # questions
        self.log('总共: %s question' % len(questions))
        for q_href in questions.xpath('div[@class="summary"]/h3/a/@href').extract():
            if q_href is not None:
                req = response.follow(q_href, callback=self.parse_question, dont_filter=True)
                self.log('question req url:%s ' % req.url)
                yield req

        # tag next page's question
        next_page = response.xpath('//div[@class="pager fl"]/a[@rel="next"]/@href').extract_first()
        if next_page is not None:
            self.log('下一页 question')
            yield response.follow(next_page, callback=self.parse_tag)

    # 某个question
    def parse_question(self, response):
        self.log('question url: %s' % response.url)
        # todo 很长的评论怎么处理的,暂时先按短评论处理
        post_user_names = response.xpath('//div[@class="user-info "]/div[@class="user-details"]/a/text()').extract()
        comment_user_names = response.xpath('//a[@class="comment-user"]/text()').extract()

        if post_user_names:
            for post_user_name in post_user_names:
                yield {
                    'name': post_user_name,
                    'src': 'StackOverflow'
                }

        if comment_user_names:
            for comment_user_name in comment_user_names:
                yield {
                    'name': comment_user_name,
                    'src': 'StackOverflow'
                }
