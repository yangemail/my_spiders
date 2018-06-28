# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from entertainment.date_utils import DateUtils
from entertainment.novel.items import BookItem, ChapterItem
import scrapy


class B23usSpider(CrawlSpider):
    name = 'b23us'
    # allowed_domains = ['23us.com']
    start_urls = ['http://23us.com/class/1_1.html']

    rules = (
        Rule(LinkExtractor(allow=r'class\/1_\d+'), follow=False),
        Rule(LinkExtractor(allow=r'book\/\d+', restrict_css='.L > a:nth-child(1)[href*=book]'),
             callback='parse_book_info'),
    )

    def parse_book_info(self, response):
        if not response.body:
            print(response.url + "已经被爬取过了，不解析Book")
        else:
            item = BookItem()
            book_url = response.url
            item['book_id'] = book_url[book_url.rfind('/') + 1:]
            item['book_name'] = response.css('h1::text').re(r'(.+) ')[0].strip()
            item['book_summary'] = response.css('#content dd > p:nth-of-type(2)::text').extract_first()

            # 页面第一行
            _1st_row = response.css('#at tr:nth-child(1)')
            item['book_author'] = _1st_row.css('td:nth-of-type(2)::text').extract_first().strip()
            item['book_category'] = _1st_row.css('td:nth-of-type(1) > a::text').extract_first()
            item['book_serial_status'] = _1st_row.css('td:nth-of-type(3)::text').extract_first().strip()
            # 页面第二行
            _2nd_row = response.css('#at tr:nth-child(2)')
            book_serial_wordcount = _2nd_row.css('td:nth-of-type(2)::text').re(r'(\d+)')[0]
            item['book_serial_wordcount'] = int(book_serial_wordcount)
            book_last_update_time = _2nd_row.css('td:nth-of-type(3)::text').extract_first().strip()
            item['book_last_update_time'] = DateUtils.parsing_date(book_last_update_time)
            # 获取章节列表
            chapter_list_url = response.css('.btnlinks a.read::attr(href)').extract_first()
            item['book_chapters_url'] = chapter_list_url

            yield item

        # 图书的章节列表页面
        yield scrapy.Request(chapter_list_url, callback=self.parse_book_chapters,)

    # 获取全部章节
    def parse_book_chapters(self, response):
        sequence = 0
        chapters = response.css('table td.L > a')
        for chapter in chapters:
            partial_url = chapter.css('::attr(href)').extract_first()
            chapter_url = response.url + partial_url
            sequence += 1
            yield scrapy.Request(chapter_url, callback=self.parse_content,
                                 meta={'sequence': sequence})

            break

    # 获取文章内容
    def parse_content(self, response):
        if not response.body:
            print(response.url + "已经被爬取过了，跳过")
            return

        chapter_name = response.css('h1::text').extract_first().strip()

        chapter_url = response.url
        chapter_id = chapter_url[chapter_url.rfind('/') + 1:chapter_url.rfind('.')]
        chapter_url = chapter_url[:chapter_url.rfind('/')]
        book_id = chapter_url[chapter_url.rfind('/') + 1:]

        item = ChapterItem()
        item['book_id'] = book_id
        item['chapter_id'] = chapter_id
        item['chapter_name'] = chapter_name
        item['chapter_sequence'] = response.meta['sequence']
        item['chapter_seq_chinese'] = None

        chapter_content = response.css('dd#contents::text').extract()
        item['chapter_content'] = '\n   '.join(chapter_content)
        item['chapter_url'] = response.url
        item['chapter_is_update_required'] = False
        item['chapter_last_update_time'] = None
        return item


if __name__ == "__main__":
    text = '2018-06-28'
    print(DateUtils.parsing_date(text))
