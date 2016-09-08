#  -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import tweepy
import api_twitter
import db_mongo
import re
import time


def load_friend_training_set(api, id, num = 5):
    """
    Gets a user's specified number of tweet as training set
    :param api:
    :param id: Specific id
    :param num: number of tweet per user
    :return:tweet list
    """
    result = []
    for status in tweepy.Cursor(api.user_timeline,id).items(num):
        result.append(status.text)
    return result


def load_friends_training_set(api, tabel_name, num1, num2 = 5):
    """
    Gets specified number of users' specified number of tweet as training set
    :param api:
    :param tabel_name: user id list
    :param num1: users' number
    :param num2: number of tweet per user
    :return: tweet list
    """
    result = []
    db = db_mongo.init_db()
    coll = db_mongo.get_doc(tabel_name, db).find()
    for i in range(num1):
        print coll[i]['id']
        try:
            one_user_result = load_friend_training_set(api, coll[i]['id'], num2)
            for i in one_user_result:
                a = re.subn("[a-zA-z]+://[^\s]*","",i)
                result.append(a[0])
        except tweepy.RateLimitError:
            print "wait"
            time.sleep(15 * 60)
            print "restart"
        except tweepy.TweepError:
            print "error"
            continue
    return result
def tfidf(corpus):
    """
    Gets the TF-IDF value of each sentence in the corpus.
    :param corpus: list
    """
    vectorizer = CountVectorizer(stop_words='english', decode_error='ignore')
    x = vectorizer.fit_transform(corpus)
    a = x.toarray()
    name =  vectorizer.get_feature_names()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(a)
    return name, tfidf.toarray()


def classification(api, id):
    tweet = ""
    for status in tweepy.Cursor(api.user_timeline,id).items(5):
        tweet += status.text
    tweet = re.subn("[a-zA-z]+://[^\s]*", "", tweet)[0]
    db = db_mongo.init_db()
    coll = db_mongo.get_doc("friends_training_set", db).find()
    result = []
    for i in coll:
        result.append(i['content'])
    result.append(tweet)
    name,array = tfidf(result)
    l = list(array[len(array) - 1])
    keyword = {}
    for i in range(len(l) - 1):
        if l[i] > 0:
            print name[i]
            print l[i]
            keyword[str(name[i])] = l[i]
    keyword_sorted = sorted(keyword.iteritems(),key=lambda x:x[1],reverse=True)
    return keyword_sorted


if __name__ == "__main__":
    api = api_twitter.init_twitter()
    # result = load_friends_training_set(api, "user_1hop", 90)
    # print result
    # infos = []
    # index = 0
    # for i in result:
    #     infos.append({"id":index,"content":i})
    # db = db_mongo.init_db()
    # coll = db_mongo.get_doc("friends_training_set", db)
    # db_mongo.insert(infos,coll)
    # name, arr = tfidf(result)
    # print name
    # print arr

    key = classification(api, "AndySgd1995")
    print key