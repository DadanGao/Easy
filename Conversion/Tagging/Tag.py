# 标签类
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from Conversion.Tagging.NLP import NLP
from Input.GWT import GWTObjects


class Tag:
    def __init__(self, gwt: GWTObjects):
        # list类型，和gwt的story相同
        self.story = gwt.story
        # list类型，和gwt的scenario相同
        self.scenario = gwt.scenario
        # list类型，list中元素属性为Pre类，包含处理后的precondition和相应的Flag标签
        self.precondition = []
        # list类型，和gwt中的when相同
        self.action = gwt.when
        # list类型，和gwt中的then相同
        self.postcondition = gwt.then

    def add_pre_into_precondition(self, gwt: GWTObjects):
        '''
        将gwt对象Given的每一个都转换成Pre类，并加入到Tag类的precondition中
        :param gwt:输入的gwt对象
        '''
        nlp = NLP()
        for precond in gwt.given:
            self.precondition.append(nlp.get_tag_of_input_string(precond))

    def print_tag(self):
        print(self.story)
        print(self.scenario)
        for pre in self.precondition:
            print(pre.content)
            self.print_tag_switch(pre.flag)
        for action in self.action:
            print(action)
        for post in self.postcondition:
            print(post)


    def print_tag_switch(self, flag: int):
        '''
        flag中的switch/case
        '''
        flags = {
            0: "消极" + " " + str(flag),
            1: "积极" + " " + str(flag),
            2: "不是分支条件",
            3: "GLOBAL 分支条件"
        }
        print(flags.get(flag))