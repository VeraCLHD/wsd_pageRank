#!/usr/bin/python
# Python 2.7

from Word import Word
from Node import Node
from Graph import Graph
from collections import deque
import sys
import re

class WordNetSearcher:
	indexFiles = ["data/index.noun", "data/index.verb", "data/index.adv", "data/index.adj"]
	dataFiles = ["data/data.noun", "data/data.verb", "data/data.adv", "data/data.adj"]
	# key: word, value: list of synsets from index file
	indexDictionary = {}
	# key: synset, value: list of related synsets
	dataDictionary = {}
	#input: list of word objects
	def __init__(self, inputWords):
		self.inputWords = inputWords
		self.synsets = set()
		self.deadSentence = False
	
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
	def getDataDictionary():
		return WordNetSearcher.dataDictionary
	
	@staticmethod
	def readIndexFiles():
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
			dict[lemma].update(synsets)
		else:
			WordNetSearcher.getIndexDictionary().setdefault(lemma, synsets)
	
	@staticmethod
	def readDataFiles():
		for dataFile in WordNetSearcher.dataFiles:
			file = open(dataFile, 'r')
			lines = file.readlines()
			for line in lines:
				if not line.startswith("  "):
					line = line.strip(" \t\n\r")
					WordNetSearcher.findAllSemanticRelationsForSynset(line)
	
	@staticmethod	
	def findAllSemanticRelationsForSynset(lineAsString):
		synset = lineAsString[0:8]
		#find all 8 digit numbers in the line that are not the synset itself
		semRelations = set([m for m in re.findall("[0-9]{8}", lineAsString) if m != synset])
		dict = WordNetSearcher.getDataDictionary()
		if synset in dict:
			dict[synset].update(semRelations)
		else:
			WordNetSearcher.getDataDictionary().setdefault(synset, semRelations)

	def getMeaningsForWord(self, word):
		wordfoundInWordnet = False
		lemma = word.getName()
		dict = WordNetSearcher.getIndexDictionary()
		if lemma and lemma in dict:
			word.getSynsets().update(dict[lemma])
			self.getSynsets().update(dict[lemma])
		else:
			word.setDeadWord(True)
			sys.stderr.write("This word is empty or was not found in WordNet 2.1")
	
	def createInitialTreeDraft(self):
		# should create a tree for each synset
		nodes = []
		for word in self.inputWords:
			wordString = word.getName()
			if not word.deadWord:
				wordNode = Node(wordString)
				self.getMeaningsForWord(word)
				synsetsForWord = word.getSynsets()
				for synset in synsetsForWord:
					semanticRelations = WordNetSearcher.dataDictionary[synset]
					# in class node, neighbours should be a set
					wordNode.getNeighbours().extend(semanticRelations)
				nodes.append(wordNode)
			if nodes:
				return Graph(self.inputWords, nodes, 0.85)
			else:
				std.err.write("This sentence cointains only dead words. No graph could be created")
				self.deadSentence = True
	
	def breadthFirstSearch(self, graph, startnode):
		nodes = graph.nodes
		visited = [False]*len(nodes)   # Flags, welche Knoten bereits besucht wurden
		q = deque()                    # Queue fur die zu besuchenden Knoten
		q.append(startnode)            # Startknoten in die Queue einf
		while len(q) > 0:              # Solange es noch unbesuchte Knoten gibt
			node = q.popleft()         # Knoten aus der Queue nehmen (first in - first out)
			if not visited[node]:      # Falls node noch nicht (auf einem anderen Weg) besucht wurde
				visited[node] = True  # Markiere node als besucht
				print node            # Drucke Knotennummer
				for neighbor in graph[node]:    # f Nachbarn in die Queue ein
					q.append(neighbor)
	

if __name__ == "__main__":
	#mock of word objects as input
	#word1 = Word("athletic_game")
	#word2 = Word("cat")
	word3 = Word("cat")
	listOfAnimals = [word3] # reference to object
	wordsearcher = WordNetSearcher(listOfAnimals)
	
	WordNetSearcher.readIndexFiles()
	WordNetSearcher.readDataFiles()
	graph = wordsearcher.createInitialTreeDraft()
	#if graph != None:
	#	for node in graph.nodes:
	#		print node.name
	#		print node.neighbours
	# graph = [[2,3],[4,5,1],[6,7,4,1],[2,3],[2],[3],[3]]
	# startnode = 1
	# visited = [False]*len(graph)   # Flags, welche Knoten bereits besucht wurden
	# q = deque()                    # Queue fur die zu besuchenden Knoten
	# q.append(startnode)            # Startknoten in die Queue einf
	# while len(q) > 0:              # Solange es noch unbesuchte Knoten gibt
		# node = q.popleft()         # Knoten aus der Queue nehmen (first in - first out)
		# if not visited[node]:      # Falls node noch nicht (auf einem anderen Weg) besucht wurde
			# visited[node] = True  # Markiere node als besucht
			# print node            # Drucke Knotennummer
			# for neighbor in graph[node]:    # f Nachbarn in die Queue ein
				# q.append(neighbor)