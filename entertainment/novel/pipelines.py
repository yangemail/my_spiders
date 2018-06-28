# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from entertainment.novel.items import BookItem, ChapterItem
from entertainment.novel.mongo_helper import MongoHelper


class NovelPipeline(object):
    collection_name = 'novel'

    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            is_exist = MongoHelper().check_is_exist(item['book_name'], item['book_author'])
            if is_exist:
                print(u'已经存在了')
                raise DropItem("Duplicate item found: %s" % item)
            else:
                MongoHelper().save_novel(item)
                print(u'开始存小说')
                return item

        if isinstance(item, ChapterItem):
            MongoHelper().save_chapter(item)
            print(u'{} 存储完毕', item['chapter_name'])
            return item
