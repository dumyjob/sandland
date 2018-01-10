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
class UsNameSpider(scrapy.Spider):
    name = 'us_name'
    allowed_domains = ['https://stackoverflow.com/tags']
    start_urls = ['http://https://stackoverflow.com/tags/']

    def parse(self, response):
        tags = response.xpath('//div[@class="tags_list"]/table[@id="tags-browser"]/tr/td[@class="tag-cell"]')

        # tag_list
        for tag in tags:
            tag_href = tag.xpath('a/@href')
            if tag_href is not None:
                yield response.follow(tag_href, self.parse_tag)

        # next tag page: tag_list
        next_page = response.xpath('//div[@class="pager fr"]/a[@rel="next"]/@href').extract_first()
        if next_page is not None and next_page.strip() != '':
            yield response.follow(next_page, self.parse)

    # 每个tag下的questions列表
    def parse_tag(self, response):
        questions = response.xpath('//div[@class="questions"]/div[@class="question-summary"]')

        # questions
        for question in questions:
            q_href = question.xpath('div[@class="summary"]/h3/a/@href')
            if q_href is not None:
                yield response.follow(q_href, self.parse_question)

        # tag next page's question
        next_page = response.xpath('//div[@class="pager fl"]/a[@rel="next"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse_tag)

    # 某个question
    def parse_question(self, response):
        # todo 很长的评论怎么处理的,暂时先按短评论处理
        post_user_names = response.xpath('//div[@class="user-info"]/div[@class="user-details"]/a/text()').extract()
        comment_user_names = response.xpath('//a[@class="comment-user"]/text()').extract()

        for post_user_name in post_user_names:
            yield {
                'name': post_user_name,
                'src': 'StackOverflow'
            }

        for comment_user_name in comment_user_names:
            yield {
                'name': comment_user_name,
                'src': 'StackOverflow'
            }
