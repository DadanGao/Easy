# NLP类
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from Input.GWT import GWTObjects
from Conversion.Tagging.Pre import Pre

# import jieba
import re

re_positive_negative_dic = re.compile('^(.+?)( [0-9]+)( .+)?$', re.U)
file_path = './positive_negative_dic'


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

    def participle(self, gwt1: GWTObjects):
        pass

    def load_pos_neg_dict(self, f):
        '''
        加载正义反义词典
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
        :return: 该段字符串的tag
        '''
        tag = -1
        for l in self.lists:
            regex = r'' + l[0]
            re_compile = re.compile(regex, re.U)
            res = re_compile.search(s1)
            if res is not None:
                tag = l[1]
                s1 = re.sub(r'' + l[0], l[2], s1)
                break
        if tag == -1:
            tag = 2
        pre1 = Pre(s1, tag)
        return pre1
