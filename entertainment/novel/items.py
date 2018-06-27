# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    # 小说编号
    novel_id = scrapy.Field()
    # 小说名字
    novel_name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 图片
    picture = scrapy.Field()
    # 内容简介
    summary = scrapy.Field()

    # 小说地址
    chapters_url = scrapy.Field()
    # 状态
    serial_status = scrapy.Field()
    # 连载字数
    serial_wordcount = scrapy.Field()
    # 文章类别
    category = scrapy.Field()
    # 最后更新
    last_update = scrapy.Field()


class ChapterItem(scrapy.Item):
    # 小说编号（和上面的小说对应）
    novel_id = scrapy.Field()
    # 用于绑定章节顺序
    sequence = scrapy.Field()
    # 章节汉字
    chapter_seq_chinese = scrapy.Field()
    # 章节名字
    chapter_name = scrapy.Field()
    # 章节内容
    chapter_content = scrapy.Field()

    # 章节地址
    chapter_url = scrapy.Field()
    # 是否已经更新
    is_update = scrapy.Field()
    # 最后更新日期
    last_updated_time = scrapy.Field()

