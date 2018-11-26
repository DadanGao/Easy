#gwt类 转换到 tag类
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Conversion.Tagging import *

class GWTToTag:
    def gwt_to_tag(self, gwtlist):
        gwtlist = gwtlist if gwtlist is not None else []
