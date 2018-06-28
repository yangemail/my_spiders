# -*- coding: utf-8 -*-

import pymongo
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
conn = pymongo.MongoClient(
    host=settings['MONGO_HOST'],
    port=settings['MONGO_PORT'],
)
database = conn.get_database(settings['MONGO_DB'])


class MongoHelper:
    # db.集合名.ensureIndex({"要设置索引的列名":1},{"unique":1})

    @classmethod
    def check_is_exist(cls, book_name, book_author):
        return database[settings['MONGO_BOOK_COLL']].find_one({"book_name": book_name, "book_author": book_author})

    @classmethod
    def save_novel(cls, item):
        database[settings['MONGO_BOOK_COLL']].insert_one(dict(item))

    @classmethod
    def save_chapter(cls, item):
        database[settings['MONGO_CONTENT_COLL']].insert_one(dict(item))
