# NLP类
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from Input.GWT import GWTObjects
from Conversion.Tagging.Pre import Pre

# import jieba
import os
import re

re_positive_negative_dic = re.compile('^(.+?)( [0-9]+)( .+)?$', re.U)
path = os.path.abspath('.')
file_path = path + '/positive_negative_dic'


class NLP:
    def __init__(self):
        '''
        lists是一个list，list中的元素是一个list1
        list1 = [原来的关键词，正反义标签，转换后的关键词]
        '''
        self.lists = []
        self.load_pos_neg_dict(file_path)

    def add_pos_neg_word(self, word=None, tag=None, sub_word=None):
        '''
        add a word into pos_neg_dictionary
        :param word:字符串
        :param tag:标志
        '''
        self.lists.append([word, tag, sub_word])

    def participle(self, gwt: GWTObjects):
        '''
        后续分词可能会使用
        '''
        pass

    def load_pos_neg_dict(self, f=file_path):
        '''
        加载正义反义词典
        使用最长匹配原则，但是没有写最长匹配代码，所以需要在字典中手动最长匹配，即同一个替换词的正反义词中长的写在前面。如下所示，不成功要放在最前面
        格式为： 正反义词（str）  词性（int） 替换后的词（str）
                不成功             0           成功
                失败              0           成功
                成功              1           成功
        :param f:词典路径
        '''
        if isinstance(f, str):
            f_name = f
            f = open(f, 'rb')
        for lineno, ln in enumerate(f, 1):
            line = ln.strip()
            if not isinstance(line, str):
                try:
                    line = line.decode('utf-8').lstrip('\ufeff')
                except UnicodeDecodeError:
                    raise ValueError('dictionary file %s must be utf-8' % f_name)
            if not line:
                continue
            word, tag, sub_word = re_positive_negative_dic.match(line).groups()
            if word is not None:
                word = word.strip()
            if tag is not None:
                tag = tag.strip()
            if sub_word is not None:
                sub_word = sub_word.strip()
            self.add_pos_neg_word(word, tag, sub_word)

    def get_tag_of_input_string(self, s1):
        '''
        :param s1: given list中的一个precondition
        :return: 该段字符串的flag
        '''
        flag = -1
        for l in self.lists:
            if 'GLOBAL' in s1:
                re.sub('GLOBAL', '', s1)
                flag = 3
                break
            regex = r'' + l[0]
            re_compile = re.compile(regex, re.U)
            res = re_compile.search(s1)
            if res is not None:
                flag = int(l[1])
                s1 = re.sub(r'' + l[0], l[2], s1)
                break
        if flag == -1:
            flag = 2
        pre1 = Pre(s1, flag)
        return pre1
