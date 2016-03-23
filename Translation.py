class Translation(object):

	def __init__(self, word, wordtype, senselist):

		# Word itself -> STR
		self.word = str(word)
		# Type of word -> STR
		self.wordtype = str(wordtype)
		# All possible senses -> List[STR]
		self.senselist = senselist
			
	# return value stuff
	def returnWord(self):
		# STR
		return self.word
	def returnWordtype(self):
		# STR
		return self.wordtype
	def returnSenselist(self):
		# List[STR]
		return self.senselist
	
	# return ALL the values
	def returnTranslation(self):
		return [self.word, self.wordtype, self.senselist]