# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # 小说编号
    book_id = scrapy.Field()
    # 小说名字
    book_name = scrapy.Field()
    # 作者
    book_author = scrapy.Field()
    # 图片
    book_image_url = scrapy.Field()
    # 内容简介
    book_summary = scrapy.Field()

    # 小说地址
    book_chapters_url = scrapy.Field()
    # 状态
    book_serial_status = scrapy.Field()
    # 连载字数
    book_serial_wordcount = scrapy.Field()
    # 文章类别
    book_category = scrapy.Field()
    # 最后更新
    book_last_update_time = scrapy.Field()


class ChapterItem(scrapy.Item):
    # 小说编号（和上面的小说对应）
    book_id = scrapy.Field()
    # 章节编号
    chapter_id = scrapy.Field()
    # 章节名字
    chapter_name = scrapy.Field()
    # 用于绑定章节顺序
    chapter_sequence = scrapy.Field()
    # 章节序号汉字
    chapter_seq_chinese = scrapy.Field()

    # 章节序号数字
    chapter_seq_number = scrapy.Field()
    # 章节内容
    chapter_content = scrapy.Field()
    # 章节地址
    chapter_url = scrapy.Field()
    # 是否需要更新
    chapter_is_update_required = scrapy.Field()
    # 最后更新日期
    chapter_last_update_time = scrapy.Field()
    # 是否异常
    chapter_is_error = scrapy.Field()

