# -*- coding: utf-8 -*-
import scrapy
from entertainment.novel.items import NovelItem, ContentItem


class A23usSpider(scrapy.Spider):
    name = '23us'
    allowed_domains = ['23us.com', 'x23us.com']
    start_urls = ['http://www.23us.com/class/1_1.html',
                  ]

    # 获得页面图书链接
    def parse(self, response):
        for book in response.xpath('//tr[@bgcolor="#FFFFFF"]'):
            # 获取章节
            novel_url = book.xpath('.//td[1]/a[2]/@href').extract()[0]

            # 获取文章简介: 需要 xpath
            # summary_url = response.xpath('.//td[1]/a[1]').extract()[0]

            item = NovelItem()
            # item['name'] = book.xpath('./td[1]/a[2]/text()').extract()[0]
            # item['author'] = book.xpath('./td[3]/text()').extract()[0]
            item['novel_url'] = novel_url
            # item['serial_status'] = book.xpath('./td[6]/text()').extract()[0]
            # item['serial_wordcount'] = book.xpath('./td[4]/text()').extract()[0]
            # item['category'] = response.css('dl#content h2').re(u'(.+) - 文章列表')[0]
            yield item

            # 获得全部章节
            yield scrapy.http.Request(url=novel_url, callback=self.parse_book_chapter)

        # TODO: 获取下一页

    # 获取全部章节
    def parse_book_chapter(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        num = 0
        allurls = response.xpath('//tr')
        for trurls in allurls:
            tdurls = trurls.xpath('./td[@class="L"]')
            for tdurl in tdurls:
                num = num + 1
                chapter_name = tdurl.xpath('.//a/text()').extract()[0]
                chapter_url = response.url + tdurl.xpath('./a/@href').extract()[0]
                self.logger.info('Got chapter url {}'.format(chapter_url))
                # 验证章节是否已经存在
                # rets = Sql.select_chapter(chapterurl)
                # if rets[0] == 1:
                #     print(u'章节已经存在了')
                #     pass
                # else:
                yield scrapy.Request(chapter_url, callback=self.parse_content,
                                     meta={'chapter_name': chapter_name, })

        # 获取文章内容

    def parse_content(self, response):
        chaptername = response.css('h1').extract()[0]
        chapter_name_by_meta = response.meta['chapter_name']

        item = ContentItem()
        contents = response.css('dd#contents').extract()
        item['chapter_content'] = '\n   '.join(contents)
        return item
