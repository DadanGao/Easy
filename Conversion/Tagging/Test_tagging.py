# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Input.file import GWTFile
from Conversion.Tagging.GWTToTagged_GWT import GWTToTag
from Conversion.BranchMerge.MergeBranch import MergeBranch

# 得到gwt文件list
path = os.path.abspath('../..')
test_path = path + '/Input'
file = GWTFile(test_path)
gwt_objects = file.get_gwt_objects()

# 进行gwt转tag对象
transformer = GWTToTag()
tag_objects = transformer.gwtlist_to_taglist(gwt_objects)
tag_objects[2].precondition[0].content = "收到位置传感器返回的值"
merge_obj = MergeBranch(tag_objects)
rucm_obj = merge_obj.rucm_obj
# print(rucm_obj.basic_obj.basic_steps_list)
# print(rucm_obj.basic_obj.postcondition)
# print(rucm_obj.basic_obj.preconditon)
# print(rucm_obj.basic_obj.story)
# print(rucm_obj.basic_obj.scenario)
#
print(rucm_obj.specific_obj_list[0].specific_RFS)
for tag in tag_objects:
    tag.print_tag()
    print()
rucm_obj.rucm_print()
