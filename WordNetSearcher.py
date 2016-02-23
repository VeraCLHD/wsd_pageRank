#!/usr/bin/python
# Python 2.7

from Word import Word
from Node import Node
from Graph import Graph
from Tree import Tree
from collections import deque
import sys
import re

class WordNetSearcher(object):
	#indexFiles = ["data/index.noun", "data/index.verb", "data/index.adv", "data/index.adj"]
	indexFiles = ["data/index.noun"]
	dataFiles = ["data/data.noun", "data/data.verb", "data/data.adv", "data/data.adj"]
	# key: word, value: list of synsets from index file
	indexDictionary = {}
	# key: synset, value: list of related synsets
	dataDictionary = {}
	#input: list of word objects
	def __init__(self, inputWords):
		self.inputWords = inputWords
		self.synsets = set()
		self.trees = []
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
		semRelations = set([m.strip() for m in re.findall("[0-9]{8}", lineAsString) if m != synset])
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
				
	def createTrees(self):
		print "CREATING SUBTREES..."
		# should create a tree for each synset
		#nodes = []
		for word in self.inputWords:
			wordString = word.getName()
			if not word.deadWord:
				self.getMeaningsForWord(word)
				synsetsForWord = word.getSynsets()
				for synset in synsetsForWord:
					synset_tree = Tree([])
					root_synset = Node(synset)
					root_synset.neighbours = WordNetSearcher.dataDictionary[synset]
					
					visited = [] # contains the node names
					q = deque()
					q.append(root_synset)
					
					while len(q) > 0:
						current_node = q.popleft()
						if current_node.name not in visited:
							visited.append(current_node.name)
							synset_tree.nodes.append(current_node) # besuchen = speichern
							
							list = []
							for neighbour in current_node.neighbours:
								list.append(neighbour_node.name)
								if neighbour !=current_node.name:
									neighbour_node = Node(neighbour)
									neighbour_node.neighbours = WordNetSearcher.dataDictionary[neighbour]
									q.append(neighbour_node)
								
					# root_synset = Node(synset)
					# root_synset.neighbours = WordNetSearcher.dataDictionary[synset]
					
					# visited = [] # contains the node names
					# q = deque()
					# q.append(root_synset)
					
					# while len(q) > 0:
						# current_node = q.popleft()
						# if current_node.name not in visited:
							# visited.append(current_node.name)
							# synset_tree.nodes.append(current_node) # besuchen = speichern
							
							# for neighbour in current_node.neighbours:
								# #if neighbour !=current_node.name:
								# neighbour_node = Node(neighbour)
								# neighbour_node.neighbours = WordNetSearcher.dataDictionary[neighbour]
								# q.append(neighbour_node)
					

def createTree(self, wurzel):
    queue = [wurzel]
    this_iteration = []
    results = [wurzel]
    iterator = 0
    while iterator < 3:
        iterator += 1
        for node in queue:
            for neighbour in WordNetSearcher.dataDictionary[node.name]:
                if not neighbour in results:
                    results.append(neighbour)
                    this_iteration.append(neighbour)
                    neighbour.tree_dictionary[wurzel] = [[node], iterator]
                else:
                    if neighbour.tree_dictionary[wurzel][1] == iterator: #diese vier zeilen braucht man um ggf das tree_dictionary um node zu erweitern
                        temp = neighbour.tree_dictionary[wurzel]
                        temp[0].append[node]
                        neighbour.tree_dictionary[wurzel] = temp
        queue = this_iteration
        this_iteration = []		
        

	def createTreesDN(self, depth):
		# should create a tree for each synset
		#nodes = []
		for word in self.inputWords:
			wordString = word.getName()
			if not word.deadWord:
				self.getMeaningsForWord(word)
				synsetsForWord = word.getSynsets()
				for synset in synsetsForWord:
					synset_tree = Tree([])
					root_synset = Node(synset)
					root_synset.neighbours = WordNetSearcher.dataDictionary[synset]
					
					elementsToDepthIncrease = len(root_synset.neighbours)
					count_elToDepthIncrease = 0
					
					visited = [] # contains the node names
					q = deque()
					q.append(root_synset)
					while len(q) >0:
						print "COUNTER: " + str(count_elToDepthIncrease)
						print "ELDEPTH INCR: " + str(elementsToDepthIncrease)
						print "DEPTH: " +  str(currentDepth)
						
						if currentDepth > depth:
							break
						if count_elToDepthIncrease == elementsToDepthIncrease:
							currentDepth +=1
							count_elToDepthIncrease = 0
						
						current_node = q.popleft()
						count_elToDepthIncrease +=1
						print "NODE:" + current_node.name
						
						if current_node.name not in visited:
							visited.append(current_node.name)
							synset_tree.nodes.append(current_node) # besuchen = speichern
							
							for neighbour in current_node.neighbours:
								neighbour_node = Node(neighbour)
								neighbour_node.neighbours = WordNetSearcher.dataDictionary[synset]
								elementsToDepthIncrease = len(neighbour_node.neighbours)
								q.append(neighbour_node)
						
	
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
	word3 = Word("cohn")
	listOfAnimals = [word3] # reference to object
	wordsearcher = WordNetSearcher(listOfAnimals)
	
	WordNetSearcher.readIndexFiles()
	WordNetSearcher.readDataFiles()
	wordsearcher.createTrees()
	#for synset in WordNetSearcher.indexDictionary[word3.name]:
	#	print "SYNSET: " + synset
	#	print WordNetSearcher.dataDictionary[synset]
	#graph = wordsearcher.createInitialTreeDraft()
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