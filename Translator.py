class Translator(object):

	def __init__(self, word, wordtype, senselists):

		# Word itself -> STR
		self.word = str(word)
		# Type of word -> STR
		self.wordtype = str(wordtype)
		# All possible senses -> List[STR]
		self.senselists = senselists
			
	# return value stuff
	def returnWord(self):
		# STR
		return self.word
	def returnWordtype(self):
		# STR
		return self.wordtype
	def returnSenselists(self):
		# List[List]
		return self.senselists
	def returnSingleSenselist(self, number):
		# List[Int]
		return self.senselists[number]
	
	
	# return ALL the values
	def returnTranslator(self):
		return [self.word, self.wordtype, self.senselists]