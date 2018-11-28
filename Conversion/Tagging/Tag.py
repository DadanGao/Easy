# 标签类
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from Conversion.Tagging.NLP import NLP
from Input.GWT import GWTObjects


class Tag:
    def __init__(self, gwt: GWTObjects):
        self.story = gwt.story
        self.scenario = gwt.scenario
        self.precondition = []
        self.action = gwt.when
        self.postcondition = gwt.then

    def add_pre_into_precondition(self, gwt: GWTObjects):
        nlp = NLP()
        for precond in gwt.given:
            self.precondition.append(nlp.get_tag_of_input_string(precond))

    def print_tag(self):
        print(self.story)
        print(self.scenario)
        for pre in self.precondition:
            print(pre.content)
            if pre.flag == '1':
                print("积极" + " " + pre.flag)
            if pre.flag == '2':
                print('不是分支条件')
            if pre.flag == '0':
                print('消极' + " " + pre.flag)
        for action in self.action:
            print(action)
        for post in self.postcondition:
            print(post)
