# !/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.linalg import norm
from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '15286059'
API_KEY = 'VyGwFUCPlIBiRPLwgsoKVnXA'
SECRET_KEY = 'a789oyNOKrIERnRzqNZgVwxDBbZeheGO'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

class similarity:
    def __init__(self):
        pass

    def tf_similarity(self, s1, s2):
        def add_space(s):
            return ' '.join(list(s))

        # 在字中间加入空格
        s1, s2 = add_space(s1), add_space(s2)
        # 转化为TF矩阵
        cv = CountVectorizer(tokenizer=lambda s: s.split())
        corpus = [s1, s2]
        vectors = cv.fit_transform(corpus).toarray()
        # 计算TF系数
        return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))

    def similar(self, s1, s2):
        if self.tf_similarity(s1, s2) >= 0.6:
            return True
        else:
            return False

    def baidu_similar(selfs, s1, s2):
        # 设置可选参数
        options = {}
        options["model"] = "CNN"
        """ 带参数调用短文本相似度 """
        dict = client.simnet(s1, s2, options)
        if dict['score'] >= 0.6:
            return True
        else:
            return False
