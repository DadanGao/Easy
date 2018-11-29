from Input.GWT import GWTObjects



class input_checker(self):
	@staticmethod
	def is_blank(self,obj):
		if obj.given[0] is 'none':
			return True
		elif obj.when[0] is 'none':
			return True
		else:
			return False

	@staticmethod
	def fill_blanks(self,obj):
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

