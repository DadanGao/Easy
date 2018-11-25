# test code:
from Input.gwt import *

file = TestGWTObjects()
objects = file.get_gwt_obj(test_obj)

for item in objects:
    print(item.given, item.when, item.then)
