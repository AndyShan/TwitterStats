#  -*- coding: utf-8 -*-
import tweepy
from tweepy import OAuthHandler
import db_mongo
import time
import fun_logging


# This part is a number of twitter api operations
# Root API is Tweepy
def init_twitter():
    """
    init tweepy server
    :return:
    """
    consumer_key = 'IrYNrMW3D6C0Zo6m1pjOwoOri'
    consumer_secret = 'wSX9lEnzckMhzUAZulilUElnFakjWQVzywuG1Ier2IRsjihTta'
    access_token = '4063096274-X1f7SZi54sMAQBOCIhL1FsKglI2MB7c5k2xcO1x'
    access_secret = 'oBdekJlB3SCXim2g7PxPZrgdyBXqTsHPeDqcHiOt8khOs'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, proxy="127.0.0.1:1080") #set proxy
    return api


def get_tweet_by_user(api,user):
    """
    Gets the tweet for the specified user
    :param api: tweepy necessary parameter
    :param user: query user id or name
    :return: specified user's Crusor
    """
    return tweepy.Cursor(api.user_timeline, id=user)


def get_user(api,user):
    """
    Gets the specified user
    :param api: tweepy necessary parameter
    :param user: query user id or name
    :return:specified user's user object
    """
    return api.get_user(user)


def get_followers(api,user):
    """
    Gets the follower for the specified user
    :param api: tweepy necessary parameter
    :param user: query user id or name
    :return: specified user's followers's array
    """
    return api.followers(user)


def get_tweet(api):
    return tweepy.Cursor(api.home_timeline)


# This part is a number of user relationship acquisition operations
# The deepest user relationship is 3_hop so far
def find_1hop_user(user_id, api):
    """
    Gets the 1hop users for the specified user
    :param user_id: query user id or name
    :param api:
    :return: user array
    """
    followers_id = api.followers_ids(user_id)
    users = []
    fun_logging.set_log("followers' id acquisition success,get" + str(len(followers_id)) + "follower id", 0)
    print "followers' id acquisition success,get" + str(len(followers_id)) + "follower id"
    index = 0
    for id in followers_id:
        print index
        index += 1
        try:
            users.append(get_user(api,id)._json)
        except tweepy.RateLimitError:
            fun_logging.set_log("RateLimitError please waiting 15 minutes", 3)
            print "RateLimitError please waiting 15 minutes"
            time.sleep(15 * 60)
            fun_logging.set_log("Re start getting data", 0)
            print "Re start getting data"
        except tweepy.TweepError:
            print "Can't get this data,user id is" + str(id)
            fun_logging.set_log("Can't get this data,user id is" + str(id),3)
            continue
    return users


def find_1hop_relationship_incoming(user_id, api):
    """
    Gets the 1hop relationship for the specified user
    :param user_id: query user id or name
    :param api:
    :return: relationship
    """
    relationship = []
    try:
        relationship_incoming = api.followers_ids(user_id)
        for r in relationship_incoming:
            relationship.append({"id":r})
    except tweepy.RateLimitError:
        fun_logging.set_log("RateLimitError please waiting 15 minutes", 3)
        print "RateLimitError please waiting 15 minutes"
        time.sleep(15 * 60)
        fun_logging.set_log("Re start getting data", 0)
        print "Re start getting data"

    return relationship


def find_2hop_relationship_incoming(user_ids, api):
    """
    Gets the 1hop relationship for the specified 1hop users
    :param user_ids: 1hop users
    :param api:
    """
    relationship = []
    index = 0
    for u in user_ids:
        print index
        index += 1
        try:
            ids = api.followers_ids(u['id'])
            print len(ids)
            lim = 0
            for i in ids:
                if (lim >100):
                    break
                lim += 1
                relationship.append({"id":i,"edge":[u['id'],i]})
            lim = 0
            db = db_mongo.init_db()
            coll = db_mongo.get_doc("relationship_2hop", db)
            db_mongo.update_relationship_2hop(relationship, coll)
            db_mongo.ensure_single(db)
            relationship = []
        except tweepy.RateLimitError:
            fun_logging.set_log("RateLimitError please waiting 15 minutes", 3)
            print "RateLimitError please waiting 15 minutes"
            time.sleep(15 * 60)
            fun_logging.set_log("Re start getting data", 0)
            print "Re start getting data"
        except tweepy.TweepError:
            print "TweepError"
            continue


def init_data(user_id, api):
    db = db_mongo.init_db()

    users = find_1hop_user(user_id, api)
    coll_user = db_mongo.get_doc("user_1hop", db)
    db_mongo.update_user(users,coll_user)

    relationship_1hop = find_1hop_relationship_incoming(user_id, api)
    coll_relationship= db_mongo.get_doc("relationship_1hop", db)
    db_mongo.update_relatioship(relationship_1hop,coll_relationship)

    print "ensure"
    db_mongo.ensure_consistency("relationship_1hop", "user_1hop", db)

    coll_relationship1_find = db_mongo.get_doc("relationship_1hop", db).find()
    find_2hop_relationship_incoming(coll_relationship1_find, api)

if __name__ == "__main__":
    api = init_twitter()
    db = db_mongo.init_db()
    # while True:
    #     init_data("AndySgd1995", api)
    #     print 1
    #     fun_logging.set_log("finished once data crawling", 0)
    #     time.sleep(24 * 60 * 60)
    coll_relationship1_find = db_mongo.get_doc("relationship_1hop", db).find()
    find_2hop_relationship_incoming(coll_relationship1_find, api)
