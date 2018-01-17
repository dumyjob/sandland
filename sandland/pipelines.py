# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from .redis_p import *


class SandlandPipeline(object):
    def process_item(self, item, spider):
        return item


# 代理IP的保存,存储到redis
# 实现效果：
# 1. 去重
# 2. 保持一定数量的可用的代理IP
# 3. 最好能够统计代理ip的存活时间
# 4. 一个hset/set保存验证可用的代理IP(只保证验证的时候是可用的,不保证持续可用); 另外一个hset/set保存
# 从代理网站爬取的代理IP. 定时xx s去验证可用代理ip hset/set中的,移除不可用的代理IP,如果发现可用代理IP
# < 警戒线值, 则去代理网站爬取代理IP,并验证可用性,加入到可用hset/set中.
# 或者一直运行一个爬虫,去代理完整爬取可用代理IP,加入到可用列表中; 一个爬虫去验证可用的代理ip,移除不可用的
# 代理IP
# 采用set还是有序set还是list
class ProxyIpPipeline(object):
    # 这里假定的item都是验证过的有效的代理IP
    def process_item(self, item, spider):
        # 将数据序列化为json后,在存入到redis中
        s = json.dumps(dict(item))
        # todo: 注意事务和并发
        r.lpush(proxy_ip_queue, s)
        return item


class UsNamePipeline(object):

    def process_item(self, item, spider):
        s = json.dumps(dict(item))
        r.sadd(us_name_key, s)

        return item



