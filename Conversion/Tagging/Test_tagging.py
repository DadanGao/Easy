# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Input.file import GWTFile
from Conversion.Tagging.GWTToTag import GWTToTag

# 得到gwt文件list
path = os.path.abspath('../..')
test_path = path + '/Input'
file = GWTFile(test_path)
gwt_objects = file.get_gwt_objects()

# 进行gwt转tag对象
transformer = GWTToTag()
tag_objects = transformer.gwtlist_to_taglist(gwt_objects)
for tag in tag_objects:
    tag.print_tag()
    print()
