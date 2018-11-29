class Pre:
    '''
    定义Tag类中precondition中的Pre类，由string和tag组成
    flag 表示 正反义， 1表示成功等; 0表示（失败/不成功）等; 2表示该条件没有分歧，是正常执行
    '''
    def __init__(self, s='', tag=1):
        self.content = s
        self.flag = tag

