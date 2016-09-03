#  -*- coding: utf-8 -*-
import pymongo
HOST = "123.206.57.111"
PORT = 27017


def init_db():
    client = pymongo.MongoClient(host=HOST, port=PORT)
    db = client['db']
    return db


def get_doc(name, db):
    return db[name]


def insert(infos, coll):
    coll.insert(infos)


if __name__ == "__main__":
    db = init_db()
    coll = get_doc("relationship_1hop",db)
    print coll.count()
