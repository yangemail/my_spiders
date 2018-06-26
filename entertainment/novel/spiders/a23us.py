# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from entertainment.novel.items import NovelItem


class A23usSpider(scrapy.Spider):
    name = '23us'
    allowed_domains = ['23us.com', 'x23us.com']
    start_urls = ['http://www.23us.com/class/1_1.html',
                  ]

    # 获得页面图书链接
    def parse(self, response):
        for book in response.xpath('//tr[@bgcolor="#FFFFFF"]'):
            # print(book.extract())
            novel_url = book.xpath('./td[1]/a[2]/@href').extract_first()

            item = NovelItem()
            item['name'] = book.xpath('./td[1]/a[2]').extract_first()
            item['novelUrl'] = novel_url
            # yield item

            # self.logger.info("---------- get novel_url %s", novel_url)
            # yield scrapy.http.Request(url=novel_url, callback=self.parse_book_chapter)
        # return scrapy.Request(url='http://www.x23us.com/html/63/63265/', callback=self.parse_book_chapter)
        yield scrapy.Request(url='http://www.x23us.com/html/63/63265/',
                             callback=self.parse_book_chapter,
                             errback=self.errback_httpbin)
        # dont_filter=True)

    def parse_book_chapter(self, response):
        # this would log http://www.example.com/some_page.html
        self.logger.info('######Got successful response from {}'.format(response.url))
        # allurls = response.xpath('//tr/td[@class="L"]')
        # for url in allurls:
        #     chaptername = url.xpath('.//a/text()').extract_first()
        #     yield {
        #         logging.log(chaptername)
        #     }

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
