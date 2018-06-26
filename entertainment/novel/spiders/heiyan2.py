# -*- coding: utf-8 -*-
import scrapy


class Heiyan2Spider(scrapy.Spider):
    name = 'heiyan2'
    allowed_domains = ['heiyan.com']
    start_urls = ['http://heiyan.com/']

    def parse(self, response):
        pass
