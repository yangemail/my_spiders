import pymongo

mongo_uri = 'mongodb://27017'
conn = pymongo.MongoClient(host='localhost', port=27017, tz_aware=False)
database = conn.get_database("entertainment")


class MongoHelper:

    @classmethod
    def check_is_exist(cls, novel_name, author):
        return database['novels'].find_one({"novel_name": novel_name, "author": author})

    @classmethod
    def save_novel(cls, item):
        database['novels'].insert_one(dict(item))

    @classmethod
    def save_chapter(cls, item):
        database['chapters'].insert_one(dict(item))
