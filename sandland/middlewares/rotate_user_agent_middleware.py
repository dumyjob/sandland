# -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random


# 轮换User-Agent中间件: 在settings.py/USER_AGENTS配置中随机选取一个User-Agent值,用来反ban.
# scrapy crawl spider1 -L WARNING,不打印Debug信息,可以清楚得看到print出来的User Agent不同
# USER_AGENTS的值都是从哪里获取的: Google anywhere
class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        # 返回的是本类的实例cls ==RandomUserAgent
        # 构造一个读取USER_AGENTS配置作为参数的实例
        # USER_AGENTS在settings.py中配置
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault(b'User-Agent', random.choice(self.user_agents))
