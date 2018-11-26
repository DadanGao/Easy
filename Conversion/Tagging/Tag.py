#标签类
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tag 表示 正反义， 1 表示成功等； 0表示（失败/不成功）等
class Pre:
    def __init__(self, s='', tag=1):
        self.content = s
        self.tag = tag


class Tag:
    def __init__(self, precondition=None, action=None, postcondition=None):
        precondition = precondition if precondition is not None else []
        action = action if action is not None else []
        postcondition = postcondition if postcondition is not None else []
        self.precondition = precondition
        self.action = action
        self.postcondition = postcondition

    def add_pre_to_precondition(self, p1):
        self.precondition.append(p1)

    def add_action(self, a1):
        self.action.append(a1)

    def add_postcondition(self, post1):
        self.postcondition.append(post1)

