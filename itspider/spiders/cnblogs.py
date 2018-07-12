# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from itspider.items import ArticleItem
from itspider.utils import md5


class Cnblogs(CrawlSpider):
    
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com']
    start_urls = (
        'https://www.cnblogs.com/',
    )
    rules = (
        Rule(LinkExtractor(allow=('.*/p/.*', )), callback='parse_item'),
    )
    download_delay = 1

    def parse_item(self, response):
        item = ArticleItem()
        item['index'] = 'article-{}'.format(self.name)
        item['document_id'] = md5(response.url)
        item['document_type'] = self.name
        item['source'] = response.url
        title = response.xpath('//title/text()').extract_first()
        title_list = title.split('-')
        item['user'] = title_list[1].strip()
        item['title'] = title_list[0].strip()
        body = response.xpath('//div[@id="cnblogs_post_body"]//text()').extract()
        item['body'] = '\n'.join(b for b in body if ''.join(b.split()))
        yield item