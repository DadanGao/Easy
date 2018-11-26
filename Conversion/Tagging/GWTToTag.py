# gwt类 转换到 tag类
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from Conversion.Tagging.Tag import Tag
from Input.GWT import GWTObjects


class GWTToTag:
    # 将gwt转换成tag
    def gwt_to_tag(self, gwt: GWTObjects):
        tag = Tag(gwt)
        tag.add_pre_into_precondition(gwt)
        return tag

    # 将输入的gwtlist转换成taglist
    def gwtlist_to_taglist(self, gwtlist):
        gwtlist = gwtlist if gwtlist is not None else []
        tag_list = []
        for gwt in gwtlist:
            tag_list.append(self.gwt_to_tag(gwt))

        return tag_list
