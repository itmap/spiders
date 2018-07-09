# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from itspider.items import ArticleItem
from itspider.utils import md5


class JuejinSpider(CrawlSpider):

    name = 'juejin'
    allowed_domains = ['juejin.im']
    start_urls = (
        'https://juejin.im/',
    )
    rules = (
        Rule(LinkExtractor(allow=('post/[a-z0-9]+?', )), callback='parse_item'),
    )

    def __init__(self, *args, **kwargs):
        super(JuejinSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        item = ArticleItem()
        item['index'] = 'article-{}'.format(self.name)
        item['document_id'] = md5(response.url)
        item['document_type'] = self.name
        item['source'] = response.url
        article = response.xpath('//article[@class="article"]')
        user = article.xpath('//div[@itemprop="author"]/meta[@itemprop="name"]/@content').extract_first()
        item['user'] = user
        title = article.xpath('//h1[@class="article-title"]/text()').extract_first()
        item['title'] = title
        body = article.xpath('//div[@class="article-content"]//text()').extract()
        item['body'] = '\n'.join(b for b in body if ''.join(b.split()))
        yield item