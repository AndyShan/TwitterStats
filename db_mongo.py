#  -*- coding: utf-8 -*-
import pymongo
HOST = ""
PORT = 27017


def init_db():
    client = pymongo.MongoClient(host=HOST, port=PORT)
    db = client['db']
    return db


def get_doc(name, db):
    return db[name]


def insert(infos, coll):
    coll.insert(infos)
