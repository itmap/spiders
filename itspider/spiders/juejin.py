# -*- coding: utf-8 -*-

import scrapy

class JuejinSpider(scrapy.Spider):
    
    name = 'juejin'
    allowed_domains = ['juejin.im']
    start_urls = (
        'https://juejin.im/?utm_source=gold_browser_extension',
    )

    def __init__(self, *args, **kwargs):
        super(JuejinSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        