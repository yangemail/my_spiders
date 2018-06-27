# -*- coding: utf-8 -*-
import scrapy
from bson import ObjectId

from entertainment.novel.items import NovelItem, ChapterItem
import uuid

from entertainment.novel.mongo_helper import MongoHelper


class A23usSpider(scrapy.Spider):
    name = '23us'
    # allowed_domains = ['23us.com', 'x23us.com']
    start_urls = ['http://www.23us.com/class/1_1.html', ]

    # 获得页面图书链接
    def parse(self, response):
        self.logger.info('## Fetching all books')
        for book in response.xpath('//tr[@bgcolor="#FFFFFF"]'):
            # 获取章节列表URL - 存到小说模型里面
            chapters_url = book.xpath('.//td[1]/a[2]/@href').extract_first()

            # 验证本书是否已经存在
            novel_name = book.xpath('.//td[1]/a[2]/text()').extract_first()
            author = book.xpath('.//td[3]/text()').extract_first()
            novel = MongoHelper().check_is_exist(novel_name=novel_name, author=author)
            if novel:
                # 目标图书存在, 获得图书 _id
                novel_id = novel['_id']
            else:
                # 获取文章简介 - （新书）
                summary_url = response.xpath('.//td[1]/a[1]/@href').extract_first()
                yield scrapy.Request(summary_url, callback=self.parse_book_summary, meta={"chapters_url": chapters_url})
                # 获取 novel_id
                novel = MongoHelper().check_is_exist(novel_name=novel_name, author=author)
                print(type(novel))

            # 获得全部章节
            yield scrapy.http.Request(chapters_url, callback=self.parse_book_chapters, meta={"novel_id": novel_id})

            # TODO
            break

        # TODO: 获取下一页

    # 获取小说概要
    def parse_book_summary(self, response):
        self.logger.info('## Fetching book summary')
        item = NovelItem()
        item['novel_name'] = response.css('h1::text').re(u'(.+) ')[0]
        # 第一行
        _1st_row = response.css('#at tr:nth-child(1)')
        item['category'] = _1st_row.css('td:nth-of-type(1)::text').extract_first()
        item['author'] = _1st_row.css('td:nth-of-type(2)::text').extract_first()
        item['serial_status'] = _1st_row.css('td:nth-of-type(3)::text').extract_first()
        # 第二行
        _2nd_row = response.css('#at tr:nth-child(2)')
        item['serial_wordcount'] = _2nd_row.css('td:nth-of-type(2)::text').extract_first()

        item['chapters_url'] = response.meta['chapters_url']
        yield item

    # 获取全部章节
    def parse_book_chapters(self, response):
        self.logger.info('## Got successful response from {}'.format(response.url))
        self.logger.info('## Fetching all chapters')

        sequence = 0
        allurls = response.xpath('//tr')
        for trurls in allurls:
            tdurls = trurls.xpath('./td[@class="L"]')
            for tdurl in tdurls:
                sequence += 1
                chapter_name = tdurl.xpath('.//a/text()/@text').extract_first()
                chapter_url = response.url + tdurl.xpath('./a/@href').extract_first()
                self.logger.info('Got chapter url {}'.format(chapter_url))
                # 验证章节是否已经存在
                # rets = Sql.select_chapter(chapterurl)
                # if rets[0] == 1:
                #     print(u'章节已经存在了')
                #     pass
                # else:
                yield scrapy.Request(chapter_url, callback=self.parse_content,
                                     meta={'chapter_name': chapter_name, 'sequence': sequence,
                                           'chapter_url': chapter_url})

                # TODO
                break
            if sequence >= 1:
                break

    # 获取文章内容
    def parse_content(self, response):
        self.logger.info('## Fetch content')
        chapter_name = response.css('h1::text').extract()[0]
        chapter_name_by_meta = response.meta['chapter_name']

        item = ChapterItem()
        item['chapter_name'] = chapter_name
        chapter_content = response.css('dd#contents::text').extract_first()
        item['chapter_content'] = chapter_content
        # item['chapter_content'] = '\n   '.join(chapter_content)
        item['chapter_url'] = response.meta['chapter_url']
        item['sequence'] = response.meta['sequence']
        return item
