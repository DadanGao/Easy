# !/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.linalg import norm


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


    def get_similiar_branches(self, gwtlist):
        '''
        需要复制gwt，进行相似度计算后分到两个list钟
        :param gwtlist:得到的gwtlist
        :return:返回两个list，一个是没有分支的gwt，一个是包含两个分支的gwt: list[][2] 0是negative 1是postitive
        '''
        pass



