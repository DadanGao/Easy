import re
import xlwt


# from Conversion.BranchMerge.BoundedFlow import BoundedFlow
# from Conversion.BranchMerge.SpecificFlow import SpecificFlow
# from Conversion.BranchMerge.GlobleFlow import GlobleFlow
# from Conversion.BranchMerge.BasicFlow import BasicFlow

class RUCM:
    def __init__(self, low_rucm):
        # 下面是整个RUCM按照正常执行的各表目属性
        # basic属性是一个字典，
        # 其中0下标对应zero，一个填补
        # pattern = re.compile(r'as a (u[\u4E00-\u9FA5]+)[,|，]I want to (u[\u4E00-\u9FA5]+)', re.I)
        pattern = re.compile(r'as a ([a-zA-Z\u4E00-\u9FA5]+)[,|，]I want to ([a-zA-Z\u4E00-\u9FA5]+)', re.I)
        m = pattern.match(low_rucm["basic_obj"].story)
        if (m):
            self.userCaseName = m.group(2)
            self.primaryActor = m.group(1)
        else:
            print("参与者和简短描述匹配失败")

        self.secondActor = None
        self.dependency = None
        self.generalization = None

        self.basic_obj = low_rucm["basic_obj"]
        self.basic_obj.basic_steps_list.pop(0)
        # 下面是分支对象列表
        self.bounded_obj_list = low_rucm["bounded_obj_list"]
        self.specific_obj_list = low_rucm["specific_obj_list"]
        # globale分支，该对象同样含有自己的pre，actions，post
        self.globale_obj_list = low_rucm["globale_obj_list"]

    # 设置表格样式
    def set_style(self, name, height, bold=False):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
        alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直方向
        style.alignment = alignment
        return style

    # 写Excel
    def saveAsFile(self, outFile):
        baseLine = 0
        f = xlwt.Workbook()
        style2 = xlwt.XFStyle()

        alignment2 = xlwt.Alignment()
        alignment2.horz = xlwt.Alignment.HORZ_LEFT  # 水平方向
        alignment2.vert = xlwt.Alignment.VERT_TOP  # 垂直方向
        style2.alignment = alignment2
        sheet1 = f.add_sheet('RUCM', cell_overwrite_ok=True)
        sheet1.col(0).width = 9000
        sheet1.col(1).width = 5000
        sheet1.col(2).width = 17000

        # row0 = ["姓名", "年龄", "出生日期", "爱好"]
        sheet1.write_merge(0, 0, 0, 2, '自动生成的RUCM文档', self.set_style('黑体', 220, True))
        colum0 = ["User Case Name", "Brief Description", "Precondition", "Primary Actor", "Secondary Actor",
                  "Dependency", "Generalization"]
        for i in range(0, len(colum0)):
            sheet1.write(i + 1, 0, colum0[i], self.set_style('Times New Roman', 220, True))
        sheet1.write_merge(1, 1, 1, 2, self.userCaseName, style2)
        sheet1.write_merge(2, 2, 1, 2, self.basic_obj.scenario, style2)
        precondition = ""
        for id, item in enumerate(self.basic_obj.precondition):
            if id == 0:
                precondition += item
            else:
                precondition += "并且"
                precondition += item
        sheet1.write_merge(3, 3, 1, 2, precondition, style2)
        sheet1.write_merge(4, 4, 1, 2, 'None' if self.primaryActor == None else self.primaryActor, style2)
        sheet1.write_merge(5, 5, 1, 2, 'None' if self.secondActor == None else self.secondActor, style2)
        sheet1.write_merge(6, 6, 1, 2, 'None' if self.dependency == None else self.dependency, style2)
        sheet1.write_merge(7, 7, 1, 2, 'None' if self.generalization == None else self.generalization, style2)
        sheet1.write_merge(8, 9 + len(self.basic_obj.basic_steps_list), 0, 0, 'Basic Flow',
                           self.set_style('黑体', 220, True))
        sheet1.write_merge(8, 8, 1, 2, 'Steps', self.set_style('宋体', 220, True))
        for id, item in enumerate(self.basic_obj.basic_steps_list):
            sheet1.write_merge(9 + id, 9 + id, 1, 2, str(id + 1) + " " + item, style2)
        sheet1.write(9 + len(self.basic_obj.basic_steps_list), 1, 'Postcondition', self.set_style('宋体', 220, True))
        postcondition = ""
        for id, item in enumerate(self.basic_obj.postcondition):
            if id == 0:
                postcondition += item
            else:
                postcondition += "并且"
                postcondition += item
        sheet1.write(9 + len(self.basic_obj.basic_steps_list), 2, postcondition, style2)
        sheet1.write_merge(10 + len(self.basic_obj.basic_steps_list), 10 + len(self.basic_obj.basic_steps_list), 0, 2,
                           '')

        baseLine = 10 + len(self.basic_obj.basic_steps_list)
        for item in self.specific_obj_list:
            sheet1.write_merge(baseLine + 1, baseLine + 2 + len(item.actions), 0, 0, 'Specific Alternative Flow',
                               self.set_style('黑体', 220, True))
            sheet1.write_merge(baseLine + 1, baseLine + 1, 1, 2, "RFS " + str(item.specific_RFS),
                               self.set_style('宋体', 220, True))
            for id, action in enumerate(item.actions):
                sheet1.write_merge(baseLine + 2 + id, baseLine + 2 + id, 1, 2, str(id + 1) + " " + action, style2)
            sheet1.write(baseLine + 2 + len(item.actions), 1, 'Postcondition', self.set_style('宋体', 220, True))
            postcondition = ""
            for id, post in enumerate(item.postcondition):
                if id == 0:
                    postcondition += post
                else:
                    postcondition += "并且"
                    postcondition += post
            sheet1.write(baseLine + 2 + len(item.actions), 2, postcondition, style2)
            sheet1.write_merge(baseLine + 3 + len(item.actions), baseLine + 3 + len(item.actions), 0, 2, '')
            baseLine += 2 + len(item.actions)
        if len(self.specific_obj_list) > 0:
            baseLine += 1

        for item in self.bounded_obj_list:
            sheet1.write_merge(baseLine + 1, baseLine + 2 + len(item.actions), 0, 0, 'Bounded Alternative Flow',
                               self.set_style('黑体', 220, True))
            rfss = ""
            for rfs in item.bound_RFS_index_list:
                rfss += str(rfs)
            sheet1.write_merge(baseLine + 1, baseLine + 1, 1, 2, "RFS " + rfss, self.set_style('宋体', 220, True))
            for id, action in enumerate(item.actions):
                sheet1.write_merge(baseLine + 2 + id, baseLine + 2 + id, 1, 2, str(id + 1) + " " + action, style2)
            sheet1.write(baseLine + 2 + len(item.actions), 1, 'Postcondition', self.set_style('宋体', 220, True))
            postcondition = ""
            for id, post in enumerate(item.postcondition):
                if id == 0:
                    postcondition += post
                else:
                    postcondition += "并且"
                    postcondition += post
            sheet1.write(baseLine + 2 + len(item.actions), 2, postcondition, style2)
            sheet1.write_merge(baseLine + 3 + len(item.actions), baseLine + 3 + len(item.actions), 0, 2, '')
            baseLine += 2 + len(item.actions)
        if len(self.bounded_obj_list) > 0:
            baseLine += 1

        for item in self.globale_obj_list:
            sheet1.write_merge(baseLine + 1, baseLine + 2 + len(item.action), 0, 0, 'Global Alternative Flow',
                               self.set_style('黑体', 220, True))
            sheet1.write_merge(baseLine + 1, baseLine + 1, 1, 2, item.precondition, self.set_style('宋体', 220, True))
            for id, action in enumerate(item.action):
                sheet1.write_merge(baseLine + 2 + id, baseLine + 2 + id, 1, 2, str(id + 1) + " " + action, style2)
            sheet1.write(baseLine + 2 + len(item.action), 1, 'Postcondition', self.set_style('宋体', 220, True))
            postcondition = ""
            for id, post in enumerate(item.postcondition):
                if id == 0:
                    postcondition += post
                else:
                    postcondition += "并且"
                    postcondition += post
            sheet1.write(baseLine + 2 + len(item.action), 2, postcondition, style2)
            sheet1.write_merge(baseLine + 3 + len(item.action), baseLine + 3 + len(item.action), 0, 2, '')
            baseLine += 2 + len(item.action)

        f.save(outFile)

    def rucm_print(self):
        print()
        print("story : ", self.basic_obj.story)
        print("scenario : ", self.basic_obj.scenario)
        print("precondition : ", self.basic_obj.precondition)
        print("BASIC FLOW")
        for i in range(0, len(self.basic_obj.basic_steps_list)):
            print("step", i + 1, " : ", self.basic_obj.basic_steps_list[i])
        print("postcondition : ", self.basic_obj.postcondition)
        print("------------------------------------------------")
        if len(self.specific_obj_list) != 0:
            for i in range(len(self.specific_obj_list)):
                print("SPECIFIC FLOW")
                print("RFS : ", self.specific_obj_list[i].specific_RFS)
                for j in range(len(self.specific_obj_list[i].actions)):
                    print("step", j, " : ", self.specific_obj_list[i].actions[j])
                print("POSTCONDITION : ", self.specific_obj_list[i].postcondition)
                print("------------------------------------------------")

        if len(self.bounded_obj_list) != 0:
            for i in range(len(self.bounded_obj_list)):
                print("BOUNDED FLOW")
                print("RFS : ", self.bounded_obj_list[i].bound_RFS_index_list)
                for j in range(len(self.bounded_obj_list[i].actions)):
                    print("step", j, " : ", self.bounded_obj_list[i].actions[j])
                print("POSTCONDITION : ", self.bounded_obj_list[i].postcondition)
                print("------------------------------------------------")

        if len(self.globale_obj_list) != 0:
            for i in range(len(self.globale_obj_list)):
                print("GLOABLE FLOW")
                print("GLOABLE CONDITION : ", self.globale_obj_list[i].precondition)
                for j in range(len(self.globale_obj_list[i].action)):
                    print("step", j, " : ", self.globale_obj_list[i].action[j])
                print("POSTCONDITION : ", self.globale_obj_list[i].postcondition)
                print("------------------------------------------------")
