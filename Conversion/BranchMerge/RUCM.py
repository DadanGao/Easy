
# from Conversion.BranchMerge.BoundedFlow import BoundedFlow
# from Conversion.BranchMerge.SpecificFlow import SpecificFlow
# from Conversion.BranchMerge.GlobleFlow import GlobleFlow
# from Conversion.BranchMerge.BasicFlow import BasicFlow

class RUCM:
    def __init__(self,low_rucm):
        #下面是整个RUCM按照正常执行的各表目属性
        #basic属性是一个字典，
        #其中0下标对应zero，一个填补
        self.basic_obj = low_rucm["basic_obj"]
        #下面是分支对象列表
        self.bounded_obj_list = low_rucm["bounded_obj_list"]
        self.specific_obj_list = low_rucm["specific_obj_list"]
        #globale分支，该对象同样含有自己的pre，actions，post
        self.globale_obj_list = low_rucm["globale_obj_list"]

    def rucm_print(self):
        print("story : ",self.basic_obj.story)
        print("scenario : ",self.basic_obj.scenario)
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

