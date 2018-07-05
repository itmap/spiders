# -*- coding: utf-8 -*-

import arrow
import json
import scrapy

from itspider.items import ArticleItem
from itspider.utils import md5


class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    allowed_domains = ['blog.csdn.net']
    start_urls = (
        'https://blog.csdn.net/',
    )
    article_list_url = 'https://blog.csdn.net/api/articles?type=more&category={category}&shown_offset={shown_offset}'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.05
    }
    categories = {}

    def __init__(self, *args, **kwargs):
        super(CsdnSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        navs = response.xpath('//nav[@id="nav"]/div/div/ul/li/a')
        for nav in navs[3:]:
            title = nav.xpath('text()').extract_first()
            url = nav.xpath('@href').extract_first()
            key = url.split('/')[-1]
            self.categories[key] = title

        for category in self.categories.keys():
            now = ''.join(str(arrow.utcnow().float_timestamp).split('.'))
            url = self.article_list_url.format(category=category, shown_offset=now)
            req = scrapy.Request(url, self.article_list)
            req.meta['category'] = category
            yield req

    def article_list(self, response):
        category = response.meta['category']
        response = json.loads(response.body)
        shown_offset = response.get('shown_offset', 0)

        for article in response.get('articles', []):
            url = article['url']
            req = scrapy.Request(url, self.article)
            req.meta['category'] = category
            req.meta['title'] = article['title']
            req.meta['user'] = article['user_name']
            yield req

        url = self.article_list_url.format(category=category, shown_offset=shown_offset)
        req = scrapy.Request(url, self.article_list)
        req.meta['category'] = category
        yield req

    def article(self, response):
        item = ArticleItem()
        item['index'] = 'article-{}'.format(self.name)
        item['document_id'] = md5(response.url)
        item['document_type'] = self.name
        item['source'] = response.url
        item['classify'] = self.categories[response.meta['category']]
        item['title'] = response.meta['title']
        item['user'] = response.meta['user']
        body = response.xpath('//article//text()').extract()
        item['body'] = '\n'.join(b for b in body if ''.join(b.split()))
        yield item
