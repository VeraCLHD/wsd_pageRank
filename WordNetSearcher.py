#!/usr/bin/python
# Python 2.7

from Word import Word
import sys

class WordNetSearcher:
	indexFiles = ["data/index.noun", "data/index.verb", "data/index.adj", "data/index.adv"]
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
		
	def getMeanings(self):
		for word in self.inputWords:
			if word.getName():
				self.readIndexFile(word)
			else:
				sys.stderr.write("this word is empty")
	
	def readIndexFile(self, word):
		wordfoundInWordnet = False
		for indexFile in WordNetSearcher.indexFiles:
			file = open(indexFile, 'r')
			lines = file.readlines()
			for line in lines:
				elements = line.strip(' \t\n\r').split(" ")
				if(elements[0] == word.getName().lower()):
					self.findSynsetsForWord(word, elements)
					wordfoundInWordnet = True
		if wordfoundInWordnet == False:
			sys.stderr.write("The word: " +  word.getName() + " was not found in WordNet 2.1")
			word.setDeadWord(True)
	
	def findSynsetsForWord(self, word, lineAsList):
		lemma = lineAsList[0]
		pnt_count = lineAsList[3]
		indexOfFirstSynset = 3 + int(pnt_count) + 3 # pnt_count is at index 3 + relations + 2 for synset count and target_synset count + 1 -> first index of synset
		synsets = lineAsList[indexOfFirstSynset:len(lineAsList)]
		if not synsets:
			word.setDeadWord(True)
		else:
			word.getSynsets().extend(synsets)
			self.getSynsets().update(synsets)
			
    def createGraph(self, words):
        #this class gets a list of words and returns a graph created on wordNet
            

if __name__ == "__main__":
	#mock of word objects as input
	word1 = Word("athletic_game")
	word2 = Word("cat")
	word3 = Word("arctonyx collaris")
	listOfAnimals = [word1, word2, word3] # reference to object
	wordsearcher = WordNetSearcher(listOfAnimals)
	wordsearcher.getMeanings()
	for word in listOfAnimals:
		print(word.getName())
		print(word.getSynsets())