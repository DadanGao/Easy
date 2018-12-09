from Conversion.Tagging.Tagged_GWTObject import Tagged_GWTObject
from Conversion.BranchMerge.BoundedFlow import BoundedFlow
from Conversion.BranchMerge.SpecificFlow import SpecificFlow
from Conversion.BranchMerge.GlobleFlow import GlobleFlow
from Conversion.BranchMerge.BasicFlow import BasicFlow
from Conversion.BranchMerge.RUCM import RUCM


# 分支合并类
class MergeBranch:
    def __init__(self, tag_list):
        # 保存每个tag的pre 状态
        state = self.tag_pre_state_list(tag_list)

        # basic_flow = []
        # used_state = [0]*len(state)
        one_state_num = 0
        for i in range(len(state)):
            if state[i] == 1:
                one_state_num += 1

        basic_dir = self.get_basic_dir(state=state, tag_list=tag_list)
        basic_obj = BasicFlow(basic_dir)

        # 标识，该小gwt整个pre list的状态，包括，整体开头为0,整体正常为1，bounded为2，specific为3，globle为4
        bound_Obj_list, specific_Obj_list, globle_Obj_list = self.get_bound_specific_globle_list(state=state,
                                                                                                 tag_list=tag_list,
                                                                                                 basic_dir=basic_dir)

        low_rucm = {}
        low_rucm["basic_obj"] = basic_obj
        low_rucm["bounded_obj_list"] = bound_Obj_list
        low_rucm["specific_obj_list"] = specific_Obj_list
        low_rucm["globale_obj_list"] = globle_Obj_list

        self.rucm_obj = RUCM(low_rucm)

    def tag_pre_state_list(self, tag_list):
        state = [0] * len(tag_list)
        for i in range(len(tag_list)):
            # pre 是每一个小gwt的pre list
            pre = tag_list[i].precondition
            # 标识，该小gwt整个pre list的状态，包括，整体开头为0,整体正常为1，bounded为2，specific为3，globle为4
            this_tag_pre_state = 0
            if len(pre) == 1:
                if int(pre[0].flag) == 0:
                    this_tag_pre_state = 3
                elif int(pre[0].flag) == 1:
                    this_tag_pre_state = 1
                elif int(pre[0].flag) == 2:
                    this_tag_pre_state = 0
                elif int(pre[0].flag) == 3:
                    this_tag_pre_state = 4
            else:
                if int(pre[-1].flag) == 1:
                    this_tag_pre_state = 1
                else:
                    if int(pre[-2].flag) == 0:
                        this_tag_pre_state = 2
                    else:
                        this_tag_pre_state = 3
            state[i] = this_tag_pre_state
            print(pre[-1].content, state[i])
        return state

    def get_basic_dir(self, state, tag_list):
        one_state_num = 0
        for i in range(len(state)):
            if state[i] == 1:
                one_state_num += 1
        print("one_state_num is ", one_state_num)
        basic_dir = {}
        basic_dir["post"] = ["zero"]
        for i in range(len(state)):
            if state[i] == 0:
                print("in state 0,i = ", i)
                basic_dir["story"] = tag_list[i].story
                basic_dir["scenario"] = tag_list[i].scenario
                pre_list = []
                for s in range(len(tag_list[i].precondition)):
                    pre_list.append(tag_list[i].precondition[s].content)
                basic_dir["preconditon"] = pre_list
                basic_dir["basic_steps_list"] = ["zero"]
                basic_dir["basic_steps_list"] += tag_list[i].action
                basic_dir["post"] = tag_list[i].postcondition
                if one_state_num != 0:
                    basic_dir["basic_steps_list"] += tag_list[i].postcondition

        cycle_num = one_state_num
        for i in range(cycle_num):
            print("cyscle num is ", cycle_num)
            for j in range(len(state)):
                if state[j] == 1:
                    print("in state 1,i = ", j)
                    one_state_num = one_state_num - 1
                    this_content = tag_list[j].precondition[-1].content
                    print("in state 1 content is : ", this_content)
                    if this_content in basic_dir["basic_steps_list"][-1]:
                        basic_dir["basic_steps_list"] += tag_list[j].action
                        if one_state_num != 0:
                            basic_dir["basic_steps_list"] += tag_list[j].postcondition
                        else:
                            print(tag_list[j].postcondition)
                            basic_dir["post"] = tag_list[j].postcondition
                            # print("postcondition = ",basic_dir["postcondition"], tag_list[i].postcondition)
        return basic_dir

    def get_bound_specific_globle_list(self, state, tag_list, basic_dir):
        bound_Obj_list = []
        specific_Obj_list = []
        globle_Obj_list = []

        for i in range(len(state)):
            # bounded RFS 确认
            if state[i] == 2:
                bound_dir = {}
                bound_RFS_index_list = []

                pre = tag_list[i].precondition
                for j in range(len(pre)):
                    for k in range(len(basic_dir["basic_steps_list"])):
                        if pre[j].content in basic_dir["basic_steps_list"][k]:
                            bound_RFS_index_list.append(k)

                bound_dir["bound_RFS_index_list"] = bound_RFS_index_list
                bound_dir["actions"] = tag_list[i].action
                bound_dir["postcondition"] = tag_list[i].postcondition

                # 用字典类型生成bounded 对象
                bound_obj = BoundedFlow(bound_dir)
                # 将该bounded 对象加入整个RUCM bounded 对象 list
                bound_Obj_list.append(bound_obj)

            # 标识，该小gwt整个pre list的状态，包括，整体开头为0,整体正常为1，bounded为2，specific为3，globle为4
            if state[i] == 3:
                specific_dir = {}
                for j in range(len(basic_dir["basic_steps_list"])):
                    if tag_list[i].precondition[0].content in basic_dir["basic_steps_list"][j]:
                        specific_dir["specific_RFS"] = j
                specific_dir["actions"] = tag_list[i].action
                specific_dir["postcondition"] = tag_list[i].postcondition

                specific_obj = SpecificFlow(specific_dir)
                specific_Obj_list.append(specific_obj)

            if state[i] == 4:
                globle_dir = {}
                globle_dir["preconditon"] = tag_list[i].precondition[0].content
                globle_dir["action"] = tag_list[i].action
                globle_dir["postcondition"] = tag_list[i].postcondition
                globle_obj = GlobleFlow(globle_dir)
                globle_Obj_list.append(globle_obj)

        return bound_Obj_list, specific_Obj_list, globle_Obj_list


if __name__ == '__main__':
    a = [1, 2, 3]
    b = [0] * len(a)
    b += a
    print(b)
