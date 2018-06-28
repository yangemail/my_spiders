import pymongo

mongo_uri = 'mongodb://27017'
conn = pymongo.MongoClient(host='localhost', port=27017, tz_aware=False)
database = conn.get_database("entertainment")


class MongoHelper:

    @classmethod
    def check_is_exist(cls, book_name, book_author):
        return database['books'].find_one({"book_name": book_name, "book_author": book_author})

    @classmethod
    def save_novel(cls, item):
        database['books'].insert_one(dict(item))

    @classmethod
    def save_chapter(cls, item):
        database['chapters'].insert_one(dict(item))
