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

        # 将字中间加入空格
        s1, s2 = add_space(s1), add_space(s2)
        # 转化为TF矩阵
        cv = CountVectorizer(tokenizer=lambda s: s.split())
        corpus = [s1, s2]
        vectors = cv.fit_transform(corpus).toarray()
        # 计算TF系数
        return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))

    def similar(self, s1, s2):
        if self.tf_similarity(s1, s2) > 0.5:
            return True
        else:
            return False
