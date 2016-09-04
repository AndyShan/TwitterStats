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


def update_user(users, coll):
    for u in users:
        id = u['id']
        coll.update({"id":id},{"$set":u},upsert=True)


def update_relatioship(relationships, coll):
    for r in relationships:
        result = coll.find_one({"id":r})
        if result == None:
            insert({"id":r},coll)

if __name__ == "__main__":
    db = init_db()
    coll = get_doc("user_1hop",db).find()
    for i in coll:
        print i