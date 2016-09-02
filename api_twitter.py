#  -*- coding: utf-8 -*-
import tweepy
from tweepy import OAuthHandler
import db_mongo
import time

def initTwiier():
    """
    初始化tweepy服务
    :return:
    """
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_secret = ''
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, proxy="127.0.0.1:1080") #设置代理
    return api

def getTweetByUser(api,user):
    """
    获取指定用户的tweet
    :param api: tweepy必要参数
    :param user: 查询用户名或ID
    :return: 指定用户的Crusor
    """
    return tweepy.Cursor(api.user_timeline, id=user)
def getUser(api,user):
    """
    获取指定用户
    :param api: tweepy必要参数
    :param user: 查询用户名或ID
    :return:指定用户User对象
    """
    return api.get_user(user)
def getfollowers(api,user):
    """
    获取指定用户的关注者
    :param api: tweepy必要参数
    :param user: 查询用户名或ID
    :return: 指定用户的关注User对象数组
    """
    return api.followers(user)
def getTweet(api):
    """
    获取eyeofthemis项目所需的tweet
    :param api: tweepy必要参数
    :return: Crusor
    """
    return tweepy.Cursor(api.home_timeline)

if __name__ == "__main__":
    api = initTwiier()
    followers_id = api.followers_ids("")
    users = []
    i = 0
    for id in followers_id:
        id = followers_id[i]
        try:
            users.append(getUser(api,id)._json)
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

    db = db_mongo.init_db()
    coll = db_mongo.get_doc("infomation",db)
    db_mongo.insert(users,coll)