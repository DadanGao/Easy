# NLP类
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from Input.GWT import GWTObjects
from Conversion.Tagging.Tag_of_precondition import Tag
from Conversion.Tagging.Tag_of_action import Tag_of_action
from Conversion.Tagging.Tag_of_postcondition import Tag_of_postcondition
from Conversion.Tagging.Similarity import similarity
from Conversion.Tagging.predict_3 import predictor
from Conversion.Tagging.Tagged_GWTObject import All_Tagged_GWTObject

import os
import re

re_positive_negative_dic = re.compile('^(.+?)( [0-9]+)( .+)?$', re.U)
path = os.path.abspath('../Tagging')
file_path = path + '/positive_negative_dic'

pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！|…|（|）'


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

    def get_flag_of_precondition(self, s1):
        '''
        积极 1
        消极 0
        global 3
        无分支 2

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
        pre1 = Tag(s1, flag)
        return pre1

    def get_type_of_precondition(self):
        pass

    def get_type_of_action(self, s1=''):
        '''
        得到
        :param s1:string, action
        :return:
        '''
        resultlist = []
        _type = ''
        if 'INCLUDE' in s1:
            _type = 'include'
            tag_action = Tag_of_action(s1, _type)
            resultlist.append(tag_action)
            return resultlist
        elif 'EXTEND' in s1:
            _type = 'extend'
            tag_action = Tag_of_action(s1, _type)
            resultlist.append(tag_action)
            return resultlist
        elif 'DO' in s1:
            sentence_list = re.split(pattern, s1)
            length = len(sentence_list)
            resultlist.append(Tag_of_action(sentence_list[0], 'do_start'))
            if 'UNTIL' in s1:
                resultlist.append(Tag_of_action(sentence_list[length - 1], 'until'))
            if length > 2:
                for i in range(1, length - 1):
                    resultlist.append(Tag_of_action(sentence_list[i], 'do_mid'))
            return resultlist

        elif '如果' in s1:
            sentence_list = re.split(pattern, s1)
            length = len(sentence_list)
            resultlist.append(Tag_of_action(sentence_list[0].replace('如果', 'IF ') + ' Then', 'if_start'))
            for i in range(1, length):
                if '如果' not in sentence_list[i]:
                    resultlist.append(Tag_of_action(sentence_list[i].replace('那么', ''), 'normal'))
                if '如果' in sentence_list[i]:
                    resultlist.append(Tag_of_action(sentence_list[0].replace('如果', 'ELSEIF ') + ' Then', 'if_mid'))
            resultlist.append(Tag_of_action('ENDIF', 'normal'))
            return resultlist
        else:
            _type = 'normal'
            tag_action = Tag_of_action(s1, _type)
            resultlist.append(tag_action)
            return resultlist

    def get_type_of_postcondition(self, s1=''):
        result_list = []
        if '验证' in s1:
            result_list.append(Tag_of_postcondition(s1, 'validation'))
        else:
            result_list.append(Tag_of_postcondition(s1, 'none_validation'))
        return result_list

    def get_similiar_precondtion_and_postcondition(self, gwtlist):
        '''
        遍历postcondition和precondition，通过相似度
        得到一个分支的前面gwt和两个分支gwt
        并将两个分支gwt的precondition变成前面gwt的postcondition
        同时使用情感分析得到分支gwt的感情，得到pre的tag对象
        :param gwtlist:
        :return:
        '''
        tagged_gwt_list = []
        simi = similarity()
        content = ''
        predictor1 = predictor()
        all_post_conditions = []
        # all_post_conditions = [post for post in [postgwt.then for postgwt in gwtlist]]
        for post in [postgwt.then for postgwt in gwtlist]:
            for item in post:
                all_post_conditions.append(item)
        for pregwt in gwtlist:
            all_tagged_gwt = All_Tagged_GWTObject(pregwt)
            for precon in pregwt.given:
                flag = -1
                for postcon in all_post_conditions:
                    if 'GLOBAL' in precon:
                        precon = re.sub('GLOBAL', '', precon)
                        flag = 3
                        pre1 = Tag(precon, flag)
                        all_tagged_gwt.precondition.append(pre1)
                        break
                    elif simi.similar(postcon, precon):
                        flag = predictor1.predict_sentence(precon)
                        content = postcon
                        pre1 = Tag(content, flag)
                        all_tagged_gwt.precondition.append(pre1)
                if flag == -1:
                    flag = 2
                    content = precon
                    pre1 = Tag(content, flag)
                    all_tagged_gwt.precondition.append(pre1)
            for action in pregwt.when:
                all_tagged_gwt.action.extend(self.get_type_of_action(action))
            for postcondition1 in pregwt.then:
                all_tagged_gwt.postcondition.extend(self.get_type_of_postcondition(postcondition1))
            tagged_gwt_list.append(all_tagged_gwt)
        return tagged_gwt_list
