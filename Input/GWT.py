# GWTObjects Class
__author__ = 'Yang Ming 2018.11.25'


class GWTObjects(object):
    def __init__(self, story_='none', scenario_='none', given_=None, when_=None, then_=None):
        if given_ is None:
            given_ = ['none', ]
        if when_ is None:
            when_ = ['none', ]
        if then_ is None:
            then_ = ['none', ]

        self.story = story_
        self.scenario = scenario_
        self.given = given_
        self.when = when_
        self.then = then_
