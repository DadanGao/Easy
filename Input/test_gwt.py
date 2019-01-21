# test code:
from Input.GWT import GWTObjects
from Input.file import GWTFile

# import from test value
test_story = 'as a 操作员，I want to 输入轧制参数'
test_scenario = '操作员向系统输入轧制过程中需要的参数，包括钢材品种、厚度及轧制精度、轧速'
test_given = ['系统已启动', '参数合法', '计算结果满足要求', '参数不合法', '计算结果不满足要求']
test_when = [['操作员打开参数输入界面', '操作员输入板坯初始数据以及轧制要求参数'],
             ['系统计算轧制力、空载辊缝、轧制速度等控轧规程', '系统显示计算结果'],
             ['操作员返回主界面'],
             ['系统显示参数输入不合法'],
             ['操作员修改计算结果']]
test_then = ['系统验证参数合法', '系统验证计算结果满足要求', '已计算出有效的控轧规程']

test_obj = [GWTObjects(test_story, test_scenario, test_given[0], test_when[0], test_then[0]),
            GWTObjects(test_story, test_scenario, test_given[1], test_when[1], test_then[1]),
            GWTObjects(test_story, test_scenario, test_given[2], test_when[2], test_then[2]),
            GWTObjects(test_story, test_scenario, test_given[3], test_when[3]),
            GWTObjects(test_story, test_scenario, test_given[4], test_when[4])]
# import from test value

# import from .txt file or path
test_path = './gwt files'
test_file = './gwt files/gwt1.txt'

file = GWTFile(test_file)
objects = file.get_gwt_objects()
if objects is not None:
    for item in objects:
        item.print_val()
# import from .txt file or path
