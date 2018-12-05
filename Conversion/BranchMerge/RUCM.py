import re
# from Conversion.BranchMerge.BoundedFlow import BoundedFlow
# from Conversion.BranchMerge.SpecificFlow import SpecificFlow
# from Conversion.BranchMerge.GlobleFlow import GlobleFlow
# from Conversion.BranchMerge.BasicFlow import BasicFlow

class RUCM:
    def __init__(self,low_rucm):
        #下面是整个RUCM按照正常执行的各表目属性
        #basic属性是一个字典，
        #其中0下标对应zero，一个填补
        #pattern = re.compile(r'as a (u[\u4E00-\u9FA5]+)[,|，]I want to (u[\u4E00-\u9FA5]+)', re.I)
        pattern = re.compile(r'as a ([a-zA-Z\u4E00-\u9FA5]+)[,|，]I want to ([a-zA-Z\u4E00-\u9FA5]+)', re.I)
        m = pattern.match(low_rucm["basic_obj"].story)
        if(m):
            self.userCaseName = m.group(2)
            self.mainActor = m.group(1)
        else: print("参与者和简短描述匹配失败")

        self.secondActor = None
        self.dependency = None
        self.generalization = None

        self.basic_obj = low_rucm["basic_obj"]
        self.basic_obj.basic_steps_list.pop(0)
        #下面是分支对象列表
        self.bounded_obj_list = low_rucm["bounded_obj_list"]
        self.specific_obj_list = low_rucm["specific_obj_list"]
        #globale分支，该对象同样含有自己的pre，actions，post
        self.globale_obj_list = low_rucm["globale_obj_list"]

    def rucm_print(self):
        print("story : ",self.basic_obj.story)
        print("scenario : ",self.basic_obj.scenario)
        print("precondition : ",self.basic_obj.precondition)
        print("BASIC FLOW")
        for i in range(1,len(self.basic_obj.basic_steps_list)):
            print("step",i," : ",self.basic_obj.basic_steps_list[i])
        print("postcondition : ",self.basic_obj.postcondition)
        print("------------------------------------------------")
        if len(self.specific_obj_list) !=0 :
            for i in range(len(self.specific_obj_list)):
                print("SPECIFIC FLOW")
                print("RFS : ",self.specific_obj_list[i].specific_RFS)
                for j in range(len(self.specific_obj_list[i].actions)):
                    print("step",j," : ",self.specific_obj_list[i].actions[j])
                print("POSTCONDITION : ",self.specific_obj_list[i].postcondition)
                print("------------------------------------------------")

        if len(self.bounded_obj_list) !=0 :
            for i in range(len(self.bounded_obj_list)):
                print("BOUNDED FLOW")
                print("RFS : ",self.bounded_obj_list[i].bound_RFS_index_list)
                for j in range(len(self.bounded_obj_list[i].actions)):
                    print("step",j," : ",self.bounded_obj_list[i].actions[j])
                print("POSTCONDITION : ",self.bounded_obj_list[i].postcondition)
                print("------------------------------------------------")

        if len(self.globale_obj_list) !=0 :
            for i in range(len(self.globale_obj_list)):
                print("GLOABLE FLOW")
                print("GLOABLE CONDITION : ",self.globale_obj_list[i].precondition)
                for j in range(len(self.globale_obj_list[i].action)):
                    print("step",j," : ",self.globale_obj_list[i].action[j])
                print("POSTCONDITION : ",self.globale_obj_list[i].postcondition)
                print("------------------------------------------------")

