# GWTObjects Class
__author__ = 'Yang Ming 2018.11.25'


class GWTObjects(object):
    def __init__(self, story_='none', scenario_='none', given_='none', when_=None, then_='none'):
        if when_ is None:
            when_ = ['none', ]
        self.story = story_
        self.scenario = scenario_
        self.given = given_
        self.when = when_
        self.then = then_

    def get_gwt_obj(self, path):
        pass


class TestGWTObjects(GWTObjects):
    def get_gwt_obj(self, obj):
        return obj


test_story = 'as a 操作员，I want to 输入轧制参数'
test_scenario = '操作员向系统输入轧制过程中需要的参数，包括钢材品种、厚度及轧制精度、轧速'
test_given = ['系统已启动', '参数合法', '计算结果满足要求', '参数不合法', '计算结果不满足要求']
test_when = [['操作员打开参数输入界面', '操作员输入板坯初始数据以及轧制要求参数'],
             ['系统计算轧制力、空载辊缝、轧制速度等控轧规程', '系统显示计算结果'],
             ['操作员返回主界面'],
             ['系统显示参数输入不合法'],
             ['操作员修改计算结果']]
test_then = ['系统验证参数合法', '系统验证计算结果满足要求', '已计算出有效的控轧规程']

test_obj = [TestGWTObjects(test_story, test_scenario, test_given[0], test_when[0], test_then[0]),
            TestGWTObjects(test_story, test_scenario, test_given[1], test_when[1], test_then[1]),
            TestGWTObjects(test_story, test_scenario, test_given[2], test_when[2], test_then[2]),
            TestGWTObjects(test_story, test_scenario, test_given[3], test_when[3]),
            TestGWTObjects(test_story, test_scenario, test_given[4], test_when[4])]
