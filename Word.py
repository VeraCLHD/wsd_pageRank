#!/usr/bin/python 
# Python 2.7


class Word:
	def __init__(self, word):
		if " " in word:
			self.name = word.replace(" ", "_")
		else:
			self.name = word
		self.synsets = set()
		# if the word has no synsets or isn't found in WordNet at all, this flag is set to True
		self.deadWord = False

	def getName(self):
		return self.name
	def getSynsets(self):
		return self.synsets
	def getDeadWord(self):
		return self.deadWord
	def setName(self, name):
		self.name = name
	def setSynsets(self, meanings):
		self.synsets = meanings
	def setDeadWord(self, deadWord):
		self.deadWord = deadWord

if __name__ == "__main__":
	word1 = Word("drive")
	list_meanings = ["bla", "bla bla"]
	print(word1.getName())
	word1.setSynsets(list_meanings)
	print(word1.getDeadWord())