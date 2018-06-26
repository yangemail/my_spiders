# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class HeiyanSpider(CrawlSpider):
    name = 'heiyan'
    allowed_domains = ['heiyan.com']
    start_urls = ['http://www.heiyan.com/all']

    rules = (
        # Loop index pages
        Rule(LinkExtractor(restrict_xpaths='//a[@class="next"]'), follow=True),
        # Get all book titles
        Rule(LinkExtractor(restrict_xpaths='//a[@class="title"]'), follow=True),
        # Get in to book details through book title
        Rule(LinkExtractor(restrict_xpaths='//a[@class="index"]'), follow=True),
        # Get all chapters
        Rule(LinkExtractor(restrict_xpaths='//a[@class="name"]'))

        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        response.xpath('//a[@class="name"]').extract_first()




