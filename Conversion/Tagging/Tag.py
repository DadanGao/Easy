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
        for precond in gwt.when:
            self.precondition.append(NLP.get_tag_of_input_string(precond))
