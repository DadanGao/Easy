from Input.GWT import GWTObjects
from jieba import jieba
import jieba.jieba.posseg as psg
test_given = ['1.系统已启动', 'a. 参数合法', 'b 计算结果满足要求', '一、参数不合法', '第五计算结果不满足要求']


def clear_s(string):
	cut_str = psg.cut(string)
	new_str = []
	st = False
	for word, flag in cut_str:
		if (flag is 'm' or flag is 'x') and st is False:
			pass
		else:
			new_str += word
			st = True
	return ''.join(new_str)


class InputChecker:
	@staticmethod
	def remove_serial(obj):
		for i in range(len(obj.given)):
			obj.given[i] = clear_s(obj.given[i])
		for i in range(len(obj.when)):
			obj.when[i] = clear_s(obj.when[i])
		for i in range(len(obj.then)):
			obj.then[i] = clear_s(obj.then[i])

	@staticmethod
	def is_blank(obj):
		if obj.given[0] is 'none':
			return True
		elif obj.when[0] is 'none':
			return True
		else:
			return False

	@staticmethod
	def fill_blanks(obj):
		story_ = 'none'
		scenario_ = 'none'
		then_ = 'none'
		for item in obj:
			if item.story != 'none':
				story_ = item.story
				break
		for item in obj:
			if item.scenario != 'none':
				scenario_ = item.scenario
				break
		for item in obj:
			if item.then != 'none':
				then_ = item.then
				break

		if story_ is 'none' or scenario_ is 'none' or then_ is 'none':
			return False
		else:
			for item in obj:
				item.story = story_
				item.scenario = scenario_
			return True

