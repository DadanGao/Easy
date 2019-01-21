# gwt类 转换到 tag类
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from Conversion.Tagging.Tagged_GWTObject import Tagged_GWTObject
from Input.GWT import GWTObjects
from Conversion.Tagging.Tagged_GWTObject import All_Tagged_GWTObject
from Conversion.Tagging.NLP import NLP


class GWTToTag:
    # 将gwt转换成tagged_gwt
    def gwt_to_tag(self, gwt: GWTObjects):
        # tagged_gwt = Tagged_GWTObject(gwt)
        # tagged_gwt.add_pre_into_precondition(gwt)
        allTagged_gwt = self.gwt_to_allTagged(gwt)
        allTagged_gwt.add_pre_into_precondition(gwt)
        allTagged_gwt.add_type_into_action(gwt)
        allTagged_gwt.add_type_into_postcondition(gwt)
        # allTagged_gwt.print_allTaggedGWTObject()
        tagged_gwt = Tagged_GWTObject(allTagged_gwt)
        return tagged_gwt

    # 将输入的gwtlist转换成tagged_gwt_list
    def gwtlist_to_taglist_reg(self, gwtlist):
        gwtlist = gwtlist if gwtlist is not None else []
        all_tagged_gwt_list = NLP().get_tagged_gwt_list_reg(gwtlist)
        tagged_gwt_list = []
        for alltaggedgwt in all_tagged_gwt_list:
            tagged_gwt_list.append(Tagged_GWTObject(alltaggedgwt))
        return tagged_gwt_list


    def gwt_to_allTagged(self, gwt: GWTObjects):
        allTagged_gwt = All_Tagged_GWTObject(gwt)
        return allTagged_gwt

    def add_type_into_precondition(self, gwtlist):
        '''
        遍历gwtlist的同时修改两个后续分支的precondition
        :param gwtlist:
        :return:
        '''
        NLP().get_similiar_precondtion_and_postcondition(gwtlist)

    # 将输入的gwtlist转换成tagged_gwt_list
    def gwtlist_to_taglist_lstm(self, gwtlist):
        gwtlist = gwtlist if gwtlist is not None else []
        all_tagged_gwt_list = NLP().get_similiar_precondtion_and_postcondition(gwtlist)
        tagged_gwt_list = []
        for alltaggedgwt in all_tagged_gwt_list:
            tagged_gwt_list.append(Tagged_GWTObject(alltaggedgwt))
        return tagged_gwt_list
