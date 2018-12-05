# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Input.file import GWTFile
from Conversion.Tagging.GWTToTag import GWTToTag
from Conversion.BranchMerge.MergeBranch import MergeBranch


# 得到gwt文件list

file = GWTFile()
file.read_file('E:\master\workspace\python\gaoruan\Easy\Input\gwt.txt')
gwt_objects = file.get_gwt_objects()

# 进行gwt转tag对象
transformer = GWTToTag()
tag_objects = transformer.gwtlist_to_taglist(gwt_objects)
tag_objects[2].precondition[0].content = "收到位置传感器返回的值"
merge_obj = MergeBranch(tag_objects)
rucm_obj = merge_obj.rucm_obj
rucm_obj.rucm_print()