# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    # 小说编号
    nameId = scrapy.Field()
    # 小说名字
    name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 小说地址
    novel_url = scrapy.Field()
    # 状态
    serial_status = scrapy.Field()
    # 连载字数
    serial_wordcount = scrapy.Field()
    # 文章类别
    category = scrapy.Field()



class ContentItem(scrapy.Item):
    # 小说编号
    id_name = scrapy.Field()
    # 章节名字
    chaptername = scrapy.Field()
    # 章节内容
    chapter_content = scrapy.Field()
    # 章节地址
    chapter_url = scrapy.Field()
    # 用于绑定章节顺序
    sequence = scrapy.Field()

