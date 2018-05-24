# -*- coding: utf-8 -*-

import scrapy

class SegmentfaultSpider(scrapy.Spider):

    name = 'segmentfault'
    allowed_domains = ['segmentfault.com']
    start_urls = (
        'https://segmentfault.com/',
    )
    base_url = 'https://segmentfault.com/api/timelines/hottest'

    def __init__(self, rid=None, *args, **kwargs):
        super(SegmentfaultSpider, self).__init__(*args, **kwargs)
        self.rid = rid

    def parse(self, response):
        page = 1
        url = '{}?page={}&_={}'.format(self.base_url, page, self.rid)
        req = scrapy.Request(url, self.article_list)
        req.headers['referer'] = 'https://segmentfault.com/'
        req.meta['page'] = page
        yield req


    def article_list(self, response):
        print response.json