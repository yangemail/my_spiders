# -*- coding: utf-8 -*-

import pymongo

from scrapy.core.downloader.handlers import http
from scrapy.utils.project import get_project_settings


class UrlFilter(object):
    # 初始化过滤器（使用mongodb过滤）
    def __init__(self):
        self.settings = get_project_settings()
        self.client = pymongo.MongoClient(
            host=self.settings['MONGO_HOST'],
            port=self.settings['MONGO_PORT']
        )
        self.db = self.client[self.settings['MONGO_DB']]
        self.bookColl = self.db[self.settings['MONGO_BOOK_COLL']]
        # self.chapterColl = self.db[self.settings['MONGO_CHAPTER_COLL']]
        self.contentColl = self.db[self.settings['MONGO_CONTENT_COLL']]

    def process_request(self, request, spider):
        if (self.bookColl.count({"novel_Url": request.url}) > 0) or (
                self.contentColl.count({"chapter_Url": request.url}) > 0):
            return http.Response(url=request.url, body=None)
