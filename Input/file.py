# GWTFile Class
__author__ = 'Yang Ming 2018.11.26'

from Input.GWT import GWTObjects
from Input.input_checker import is_blank
from Input.input_checker import fill_blanks
import re
import os
re_story = r'story'
re_scenario = r'scenario'
re_given = r'given'
re_when = r'when'
re_then = r'then'


class GWTFile:
    def __init__(self, path_='./'):
        self.__path = path_
        self.__file_name_list = []
        self.__gwt_obj = []
        self.__check_note = ''

    def get_file_names(self):
        for root, dirs, files in os.walk(self.__path):
            for file in files:
                if os.path.splitext(file)[1] == '.txt':
                    self.__file_name_list.append(os.path.join(os.path.abspath(root), file))

    def read_file(self, filename):
        f_story = f_scenario = f_given = f_when = f_then = False
        with open(filename, 'r', encoding='UTF-8') as file:
            for content in file.readlines():
                if re.match(re_story, content, re.IGNORECASE):
                    f_story = f_scenario = f_given = f_when = f_then = False
                    f_story = True
                    self.__gwt_obj.append(GWTObjects())
                elif re.match(re_scenario, content, re.IGNORECASE):
                    f_story = f_scenario = f_given = f_when = f_then = False
                    f_scenario = True
                elif re.match(re_given, content, re.IGNORECASE):
                    f_story = f_scenario = f_given = f_when = f_then = False
                    f_given = True
                elif re.match(re_when, content, re.IGNORECASE):
                    f_story = f_scenario = f_given = f_when = f_then = False
                    f_when = True
                elif re.match(re_then, content, re.IGNORECASE):
                    f_story = f_scenario = f_given = f_when = f_then = False
                    f_then = True
                elif content.strip() != '':
                    if f_story:
                        if re.match('none', self.__gwt_obj[-1].story, re.IGNORECASE):
                            self.__gwt_obj[-1].story = content.rstrip()
                        else:
                            self.__gwt_obj[-1].story += content.rstrip()
                    elif f_scenario:
                        if re.match('none', self.__gwt_obj[-1].scenario, re.IGNORECASE):
                            self.__gwt_obj[-1].scenario = content.rstrip()
                        else:
                            self.__gwt_obj[-1].scenario += content.rstrip()
                    elif f_given:
                        if re.match('none', self.__gwt_obj[-1].given[0], re.IGNORECASE):
                            self.__gwt_obj[-1].given[0] = content.rstrip()
                        else:
                            self.__gwt_obj[-1].given.append(content.rstrip())
                    elif f_when:
                        if re.match('none', self.__gwt_obj[-1].when[0], re.IGNORECASE):
                            self.__gwt_obj[-1].when[0] = content.rstrip()
                        else:
                            self.__gwt_obj[-1].when.append(content.rstrip())
                    elif f_then:
                        if re.match('none', self.__gwt_obj[-1].then[0], re.IGNORECASE):
                            self.__gwt_obj[-1].then[0] = content.rstrip()
                        else:
                            self.__gwt_obj[-1].then.append(content.rstrip())

    def gwt_check(self):
        for obj in self.__gwt_obj:
            if is_blank(obj) is True:
                obj.print_val()
                self.__check_note = "Given or When blank error!"
                return False
        if fill_blanks(self.__gwt_obj) is False:
            self.__check_note = "No Story, Scenario or Then found!"
            return False
        return True

    # return a list of gwt objects if success
    # or None if failed
    def get_gwt_objects(self):
        self.get_file_names()
        for files in self.__file_name_list:
            self.read_file(files)
        if self.gwt_check() is True:
            print(self.__check_note)
            return self.__gwt_obj
        else:
            print(self.__check_note)
            return None


