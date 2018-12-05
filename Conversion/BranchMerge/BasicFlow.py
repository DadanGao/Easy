
class BasicFlow:
    def __init__(self,basic_dir):
        self.story = basic_dir["story"]
        self.scenario = basic_dir["scenario"]
        self.precondition = basic_dir["preconditon"]
        self.basic_steps_list = basic_dir["basic_steps_list"]
        self.postcondition = basic_dir["post"]