# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from Conversion.Tagging.NLP import NLP

nlp = NLP()
nlp.load_pos_neg_dict('./positive_negative_dic')
for i in nlp.lists:
    regex = r'' + i[0]
    re_compile = re.compile(regex, re.U)
    res = re_compile.search("系统验证不成功")
    if res is not None:
        print(i[1])
        print(re.sub(r'' + i[0], i[2], "系统验证不成功"))
        break
