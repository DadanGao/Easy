# NLP类
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from Conversion.Tagging.Tag_of_precondition import Tag
from Conversion.Tagging.Tag_of_action import Tag_of_action
from Conversion.Tagging.Tag_of_postcondition import Tag_of_postcondition
from Conversion.Tagging.Similarity import similarity
from Conversion.Tagging.predict_3 import predictor
from Conversion.Tagging.Tagged_GWTObject import All_Tagged_GWTObject
from pyhanlp import *

import os
import re

re_positive_negative_dic = re.compile('^(.+?)( [0-9]+)( .+)?$', re.U)
path = os.path.abspath('../Conversion/Tagging')# 使用Django
# path = os.path.abspath('../Conversion/Tagging') #不使用Django
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
        return flag

    def get_type_of_action(self, s1=''):
        '''
        得到
        :param s1:string, action
        :return:
        '''
        s1 = self.nlp_action(s1)
        resultlist = []
        _type = ''
        # if 'INCLUDE' in s1:
        #     _type = 'include'
        #     tag_action = Tag_of_action(s1, _type)
        #     resultlist.append(tag_action)
        #     return resultlist
        # elif 'EXTEND' in s1:
        #     _type = 'extend'
        #     tag_action = Tag_of_action(s1, _type)
        #     resultlist.append(tag_action)
        #     return resultlist
        # elif 'DO' in s1:
        #     sentence_list = re.split(pattern, s1)
        #     length = len(sentence_list)
        #     resultlist.append(Tag_of_action(sentence_list[0], 'do_start'))
        #     if 'UNTIL' in s1:
        #         resultlist.append(Tag_of_action(sentence_list[length - 1], 'until'))
        #     if length > 2:
        #         for i in range(1, length - 1):
        #             resultlist.append(Tag_of_action(sentence_list[i], 'do_mid'))
        #     return resultlist

        if '如果' in s1:
            # elif '如果' in s1:
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
            sentence_list = re.split(pattern, s1)
            for i in range(0, len(sentence_list)):
                _type = 'normal'
                if sentence_list[i] == '':
                    continue
                tag_action = Tag_of_action(sentence_list[i], _type)
                resultlist.append(tag_action)
            return resultlist

    def get_type_of_postcondition(self, s1=''):
        result_list = []
        if '验证' in s1:
            result_list.append(Tag_of_postcondition(s1, 'validation'))
        else:
            result_list.append(Tag_of_postcondition(s1, 'none_validation'))
        return result_list

    def get_tagged_gwt_list_reg(self, gwtlist):
        '''
        使用reg来匹配情感
        :param gwtlist:
        :return:
        '''
        tagged_gwt_list = []
        content = ''
        all_post_conditions = []
        for post in [postgwt.then for postgwt in gwtlist]:
            for item in post:
                all_post_conditions.append(item)
        for gwt in gwtlist:
            all_tagged_gwt = All_Tagged_GWTObject(gwt)
            for precon in gwt.given:
                flag = -1
                if 'GLOBAL' in precon:
                    precon = re.sub('GLOBAL', '', precon)
                    flag = 3
                    content = precon
                    pre1 = Tag(content, flag)
                    all_tagged_gwt.precondition.append(pre1)
                for postcon in all_post_conditions:
                    if similarity().similar(precon, postcon):
                        flag = self.get_flag_of_precondition(precon)
                        content = postcon
                        pre1 = Tag(content, flag)
                        all_tagged_gwt.precondition.append(pre1)
                if flag == -1:
                    flag = 2
                    content = precon
                    pre1 = Tag(content, flag)
                    all_tagged_gwt.precondition.append(pre1)
            for action in gwt.when:
                all_tagged_gwt.action.extend(self.get_type_of_action(action))
            for postcondition1 in gwt.then:
                all_tagged_gwt.postcondition.extend(self.get_type_of_postcondition(postcondition1))
            tagged_gwt_list.append(all_tagged_gwt)
        return tagged_gwt_list

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
                        # for l in self.lists:
                        #     regex = r'' + l[0]
                        #     re_compile = re.compile(regex, re.U)
                        #     res = re_compile.search(precon)
                        #     if res is not None:
                        #         flag = int(l[1])

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

    def nlp_action(self, s1):
        '''
        对when中的每行数据进行提取，争取把信息补全，以达到比较高的适应性
        调用hanlp的依存句法分析

        eg1：正常的主谓宾短语
        输入：用户输入账号

        处理过程：
        用户 -- 主谓关系
        输入 -- 核心关系
        账号 -- 动宾关系

        输出：用户输入账号

        eg2:
        输入： 用户输入账号、密码 or 用户输入账号和密码

        处理过程：
        用户 -- 主谓关系
        输入 -- 核心关系
        账号 -- 动宾关系
        、 -- 标点符号           和 -- 左附加关系
        密码 -- 并列关系

        输出：1 用户输入账号
            2 用户输入密码

        eg3:
        输入：用户输入账号和密码，点击取钱，输入取款金额

        处理过程：
        用户 -- 主谓关系
        输入 -- 核心关系
        账号 -- 动宾关系
        和 -- 左附加关系
        密码 -- 并列关系
        ， -- 标点符号
        点击 -- 并列关系
        取钱 -- 动宾关系
        ， -- 标点符号
        输入 -- 并列关系
        取款 -- 定中关系
        金额 -- 动宾关系

        输出：
        用户输入账号
        用户输入密码
        用户点击取钱
        用户输入取款金额

        eg4: 不同主语
        输入：用户输入账号和密码，系统显示取钱页面

        处理过程：用户 --(主谓关系)--> 输入
        输入 --(核心关系)--> ##核心##
        账号 --(动宾关系)--> 输入
        和 --(左附加关系)--> 密码
        密码 --(并列关系)--> 账号
        ， --(标点符号)--> 输入
        系统 --(主谓关系)--> 显示
        显示 --(并列关系)--> 输入
        取钱 --(定中关系)--> 页面
        页面 --(动宾关系)--> 显示

        输出：
        用户输入账号
        用户输入密码
        系统显示取钱页面

        eg5：if else
        输入： 如果执行预计算，则预期预计算路径成功，客户确认路径，点击应用。如果不执行预计算，则客户点击应用

        处理过程：
        如果 --(状中结构)--> 执行
        执行 --(核心关系)--> ##核心##
        预计算 --(动宾关系)--> 执行
        ， --(标点符号)--> 执行
        则 --(状中结构)--> 预期
        预期 --(并列关系)--> 执行
        预计算 --(定中关系)--> 路径
        路径 --(主谓关系)--> 成功
        成功 --(动宾关系)--> 预期
        ， --(标点符号)--> 预期
        客户 --(主谓关系)--> 确认
        确认 --(并列关系)--> 预期
        路径 --(动宾关系)--> 确认
        ， --(标点符号)--> 确认
        点击 --(并列关系)--> 确认
        应用 --(动宾关系)--> 点击
        。 --(标点符号)--> 执行
        如果 --(状中结构)--> 执行
        不 --(状中结构)--> 执行
        执行 --(并列关系)--> 执行
        预计算 --(动宾关系)--> 执行
        ， --(标点符号)--> 执行
        则 --(状中结构)--> 点击
        客户 --(主谓关系)--> 点击
        点击 --(并列关系)--> 执行
        应用 -- (并列关系)--> 点击

        输出：
        如果执行预计算，则预期预计算路径成功，客户确认路径，客户点击应用。如果不执行预计算，则客户点击应用


        :param s1: gwtobejct中的when的每个数据
        :return: 返回修改后的action列表
        '''
        temp = HanLP.parseDependency(s1)
        word_array = temp.getWordArray()
        # for word in word_array:
        #     print("%s --(%s)--> %s" % (word.LEMMA, word.DEPREL, word.HEAD.LEMMA))
        # print(len(word_array))
        # print()

        result = ''  # 返回的结果str
        user = ''  #
        action = ''  # 动作
        pre = 1
        mid = 1
        post = 1
        temp_pre = ''
        temp_mid = ''
        temp_post = ''
        suffix = '{'
        i = 0
        if len(word_array) == 1:
            return word_array[0].LEMMA
        while i < len(word_array):
            if word_array[i].DEPREL == '主谓关系':
                user = word_array[i].LEMMA
                i += 1
                pre = 0
                continue
            if word_array[i].DEPREL == "核心关系":
                action = word_array[i].LEMMA
                i += 1
                mid = 0
                continue
            if word_array[i].DEPREL == "动宾关系":
                result += temp_pre + user + temp_mid + action + temp_post + word_array[i].LEMMA + suffix
                i += 1
                post = 0
                continue
            if word_array[i].DEPREL == "并列关系":
                temp = word_array[i].HEAD
                pre = 0
                while temp.DEPREL != '核心关系' and temp.DEPREL != '动宾关系' and temp.DEPREL is not None:
                    temp = temp.HEAD
                if temp.DEPREL == '核心关系':
                    action = word_array[i].LEMMA
                    mid = 0
                    i += 1
                    continue
                if temp.DEPREL == "动宾关系":
                    result += temp_pre + user + temp_mid + action + temp_post + word_array[i].LEMMA + suffix
                    i += 1
                    post = 0
                    continue
                i += 1
            if word_array[i].DEPREL == "标点符号":
                if pre + mid + post >= 1:
                    result += temp_pre + user + temp_mid + action + temp_post + suffix
                pre = mid = post = 1
                temp_pre = temp_post = temp_mid = ""
                i += 1
                continue
            if word_array[i].DEPREL == "左附加关系":
                post = 1
                i += 1
                continue
            if pre == 1:
                temp_pre += word_array[i].LEMMA
                i += 1
                pre = 0
                continue
            if mid == 1:
                temp_mid += word_array[i].LEMMA
                i += 1
                continue
            if post == 1:
                temp_post += word_array[i].LEMMA
                i += 1
                continue
            i += 1
        return result


if __name__ == "__main__":
    nlp = NLP()
    s1 = "用户输入账号与密码"
    print(nlp.nlp_action(s1))
