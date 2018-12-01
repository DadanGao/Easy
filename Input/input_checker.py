from Input.GWT import GWTObjects
from jieba import jieba
import jieba.jieba.posseg as psg
test_given = ['1.系统已启动', 'a.参数合法', 'b 计算结果满足要求', '一、参数不合法', '计算结果不满足要求']


def copy_string(cut_str):
	result = ['', ]
	for word in cut_str:
		result.append(word)
	return "".join(result)


def clear_s(string):
	cut_str = psg.cut(string)
	for word, flag in cut_str:
		if flag is 'm' or flag is 'n' or flag is 'x' or flag is 'eng':
			pass
		else:
			copy_string(cut_str)
			break
	print("".join(cut_str))


for item in test_given:
	clear_s(item)


class InputChecker:
	@staticmethod
	def remove_serial(obj):
		for given in obj.given:
			clear_s(given)
		for when in obj.when:
			clear_s(when)
		for then in obj.then:
			clear_s(then)

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

