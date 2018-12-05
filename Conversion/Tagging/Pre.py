class Pre:
    '''
    定义Tag类中precondition中的Pre类，由string和tag组成
    flag 表示 正反义， 1表示成功等; 0表示（失败/不成功）等; 2表示该条件没有分歧，是正常执行; 3 表示是全局分支前提条件，global

    gwt1
    系统正在运行
    不是分支条件

    gwt2
    收到位置传感器返回的值
    积极 1

    gwt3
    系统收到位置传感器返回的值
    消极 0

    gwt4
    操作员退出 GLOBAL
    GLOBAL 分支条件
    '''
    flag: int;

    def __init__(self, s='', tag=1):
        # str类型，将gwt对象的given list处理后得到的内容
        # 其中为了后续分支合并的方便，Pre.content中已经做了同义词、近义词、反义词的同一化处理，即用一个词表示。
        # 在content使用同一个词表示后，使用flag标识原来given中的语义，积极、消极、无分支和全局分支
        self.content = s
        self.flag = tag

