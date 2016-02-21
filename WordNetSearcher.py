#!/usr/bin/python
# Python 2.7

from Word import Word
import sys

class WordNetSearcher:
	indexFiles = ["data/index.noun", "data/index.verb", "data/index.adv", "data/index.adj"]
	# key: word, value: list of synsets
	indexDictionary = {}
	#input: list of word objects
	def __init__(self, inputWords):
		self.inputWords = inputWords
		self.synsets = set()
	
	def getSynsets(self):
		return self.synsets
	def setSynsets(self, meanings):
		self.synsets = meanings
	def getWords(self):
		return self.inputWords
	def setWords(self, inputWords):
		self.inputWords = inputWords
	
	@staticmethod
	def getIndexDictionary():
		return WordNetSearcher.indexDictionary
	
	@staticmethod
	def readIndexFile():
		for indexFile in WordNetSearcher.indexFiles:
			file = open(indexFile, 'r')
			lines = file.readlines()
			for line in lines:
				if not line.startswith("  "):
					elements = line.strip(" \t\n\r").split(" ")
					WordNetSearcher.findAllSynsetsForIndexLine(elements)
	@staticmethod	
	def findAllSynsetsForIndexLine(lineAsList):
		lemma = lineAsList[0]
		pnt_count = lineAsList[3]
		indexOfFirstSynset = 3 + int(pnt_count) + 3 # pnt_count is at index 3 + relations + 2 for synset count and target_synset count + 1 -> first index of synset
		synsets = set(lineAsList[indexOfFirstSynset:len(lineAsList)])
		dict = WordNetSearcher.getIndexDictionary() 
		if lemma in dict:
			#print lemma + " " + str(dict[lemma])
			dict[lemma].update(synsets)
		else:
			WordNetSearcher.getIndexDictionary().setdefault(lemma, synsets)
	
	def getMeaningsForAllWords(self):
		for word in self.inputWords:
			wordfoundInWordnet = False
			lemma = word.getName()
			dict = WordNetSearcher.getIndexDictionary()
			if lemma and lemma in dict:
				word.getSynsets().update(dict[lemma])
				self.getSynsets().update(dict[lemma])
			else:
				word.setDeadWord(True)
				sys.stderr.write("This word is empty or was not found in WordNet 2.1")

if __name__ == "__main__":
	#mock of word objects as input
	word1 = Word("athletic_game")
	word2 = Word("cat")
	word3 = Word("arctonyx collaris")
	listOfAnimals = [word1, word2, word3] # reference to object
	wordsearcher = WordNetSearcher(listOfAnimals)
	
	WordNetSearcher.readIndexFile()
	wordsearcher.getMeaningsForAllWords()
	print wordsearcher.getSynsets()
	# d = set()
	# d.add(1)
	# print(d)
	# list = [1,2,3,4]
	# s = set(list)
	# s.update([5, 4])
	# print(s)