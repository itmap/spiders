# -*- coding: utf-8 -*-

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    user = scrapy.Field()
    body = scrapy.Field()
    classify = scrapy.Field()
    index = scrapy.Field()
    document_id = scrapy.Field()
    document_type = scrapy.Field()
