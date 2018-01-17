# -*- coding: utf-8 -*-
import logging
import time
from scrapy import signals
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


# 统计每一条爬取的时间, 每100条统计一下平均时间
class LogTimeExtension(object):

    def __init__(self, batch_count):
        self.batch_count = batch_count
        self.items_scraped = 0
        # 上一批完成的时间,在spider开始的时候初始化时间
        # 在完成一批后,获取/更新时间
        self.pre_batch_done_time = None

    @classmethod
    def from_crawler(cls, crawler):
        # get the number of items from settings
        # item_count = crawler.settings.getint('BOLO_BATCH', 1000)

        # instantiate the extension object
        ext = cls(100)

        # connect the extension object to signals

        # crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        # crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.per_item_start, signal=signals.request_scheduled)
        crawler.signals.connect(ext.per_item_done_failure, signal=signals.spider_error)
        crawler.signals.connect(ext.per_item_done_success, signal=signals.response_received)
        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info('spider start')
        self.pre_batch_done_time = time.time()

    def per_item_start(self, request, spider):
        logger.info('request start')
        request.meta['start_time'] = time.time()

    def per_item_done_failure(self, failure, response, spider):
        rcv_time = time.time()
        start_time = response.request.meta['start_time']

        time_elapsed = rcv_time - start_time

        logger.info('got response, time elapsed: %0.2f' % time_elapsed)

        self.items_scraped += 1

        if self.items_scraped % self.batch_count == 0:
            # 已经完成一批
            cur_batch_done_time = time.time()
            time_elapsed = cur_batch_done_time - self.pre_batch_done_time
            logger.info('batch size: %s, pre batch done at: %0.2f, cur batch done at: %0.2f, elapsed: %0.2f'
                        % (self.batch_count, self.pre_batch_done_time, cur_batch_done_time, time_elapsed))

            self.pre_batch_done_time = cur_batch_done_time


    def per_item_done_success(self, response, request, spider):
        rcv_time = time.time()
        start_time = request.meta['start_time']

        time_elapsed = rcv_time - start_time

        logger.info('got response, time elapsed: %0.2f' % time_elapsed)

        self.items_scraped += 1

        if self.items_scraped % self.batch_count == 0:
        # 已经完成一批
            cur_batch_done_time = time.time()
            time_elapsed = cur_batch_done_time - self.pre_batch_done_time
            logger.info('batch size: %s, pre batch done at: %0.2f, cur batch done at: %0.2f, elapsed: %0.2f'
                        % (self.batch_count, self.pre_batch_done_time, cur_batch_done_time, time_elapsed))

            self.pre_batch_done_time = cur_batch_done_time


