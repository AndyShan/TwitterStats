#  -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import tweepy


def load_friends_training_set(api):
    result = []
    for status in tweepy.Cursor(api.home_timeline).items(2):
        result.append(status.text)
    return result

def tfidf(corpus):
    """
    获取语料库中每一个句子的tf-idf值
    :param corpus: 语料库
    """
    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(corpus)
    a = x.toarray()
    name =  vectorizer.get_feature_names()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(a)
    return name, tfidf.toarray()
