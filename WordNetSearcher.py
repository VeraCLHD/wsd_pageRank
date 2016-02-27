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
		self.inputWords = []
		for word in inputWords:
			self.inputWords.append(Word(word))
		self.synsets = set()
		self.raw_trees = []
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
	
	def createTree(self, wurzel):
		queue = [wurzel]
		this_iteration = []
		results = [wurzel]
		iterator = 0
		while iterator < 3:
			iterator += 1
			for node in queue:
				for neighbour in WordNetSearcher.dataDictionary[node.name]:
					
					neighbour_node = Node(neighbour)
					neighbour_node.neighbours = WordNetSearcher.dataDictionary[neighbour]
					
					if not neighbour_node in results:
						results.append(neighbour_node)
						this_iteration.append(neighbour_node)
						neighbour_node.tree_dictionary[wurzel] = [[node], iterator]
					else:
						if neighbour_node.tree_dictionary[wurzel][1] == iterator: #diese vier zeilen braucht man um ggf das tree_dictionary um node zu erweitern
							temp = neighbour_node.tree_dictionary[wurzel]
							temp[0].append[node]
							neighbour_node.tree_dictionary[wurzel] = temp
			queue = this_iteration
			this_iteration = []
		self.raw_trees.append(Tree(results))
		
				
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
					root_synset = Node(synset)
					root_synset.neighbours = WordNetSearcher.dataDictionary[synset]
					self.createTree(root_synset)
	
	# def constructGraph(self):
		# # if no trees were constructed because of dead words
		# if len(self.raw_trees) == 0:
			# return Graph(self.inputWords, [], 0.85)
		# # if only one tree is constructed, then this is our graph
		# elif len(self.raw_trees) == 1:
			# setOfNodes = set(self.raw_trees[0].nodes)
			# listOfNodes = list(setOfNodes)
			# return Graph(self.inputWords, listOfNodes, 0.85)
		# else:
			# relevant_nodes = set()
			# no_common_nodes = True
			# #raw trees are the subtrees extracted with breadth first search
			# for i in range(0,len(self.raw_trees)):
				# tree_1 = self.raw_trees[i]
				# for k in range(i, len(self.raw_trees)):
					# tree_2 = self.raw_trees[k]
					# # no comparison of tree with itself
					# if tree_1 != tree_2:
						# for node in tree_1.nodes:
							# if node in tree_2.nodes:
								# no_common_nodes = False
								# tree_1_root = tree_1.nodes[0]
								# tree_2_root = tree_2.nodes[0]
								# # only if the two synsets aren't from the same word
								# if self.checkTreesAssignmentToWord(tree_1_root, tree_2_root) == False:
									# # process node from tree 2
									# for relevant_node in node.tree_dictionary.keys():
										# #saved the common node and its root from tree_2
										# relevant_nodes.update(relevant_node)
										# relevant_nodes.update(tree_1_root)
										# length = node.tree_dictionary[tree_1_root][1] # path length
										# if length == 2:
											# path_to_root_node = node.tree_dictionary[tree_1_root][0]
											# relevant_nodes.update(path_to_root_node)
										# elif length == 3:
											# path_to_root_node = node.tree_dictionary[tree_1_root][0]
											# relevant_nodes.update(path_to_root_node)
											# path_to_root_node_2 = path_to_root_node.tree_dictionary[tree_1_root][0]
											# relevant_nodes.update(path_to_root_node_2)
										
									# #same node is also in tree 2
									# node_2 = tree_2[tree_2.index(node)]
									# for relevant_node_2 in node_2.tree_dictionary.keys():
										# relevant_nodes.update(relevant_node_2)
										# relevant_nodes.update(tree_2_root)
										# length_2 = node_2.tree_dictionary[tree_2_root][1] # path length
										# if length_2 == 2:
											# path_to_root_node_21 = node_2.tree_dictionary[tree_2_root][0]
											# relevant_nodes.update(path_to_root_node_21)
										# elif length_2 == 3:
											# path_to_root_node_21 = node_2.tree_dictionary[tree_2_root][0]
											# relevant_nodes.update(path_to_root_node_21)
											# path_to_root_node_3 = path_to_root_node_21.tree_dictionary[tree_2_root][0]
											# relevant_nodes.update(path_to_root_node_3)
			
			# if no_common_nodes == True:
				# for tree in self.raw_trees:
					# relevant_nodes.update(tree.nodes)
			# graph = Graph(self.inputWords, list(relevant_nodes), 0.85)	
			# return graph
					
	# def checkTreesAssignmentToWord(self, tree_1_root, tree_2_root):
		# for word in self.inputWords:
			# #if it returns true, then the synsets are from the same word
			# return (tree_1_root in word.synsets and tree_2_root in word.synsets)
	
	def constructGraph2(self, d):
		# if no trees were constructed because of dead words
		if len(self.raw_trees) == 0:
			return Graph(self.inputWords, [], d)
		# if only one tree is constructed, then this is our graph
		elif len(self.raw_trees) == 1:
			setOfNodes = set(self.raw_trees[0].nodes)
			listOfNodes = list(setOfNodes)
			return Graph(self.inputWords, listOfNodes, d)
		else:
			relevant_nodes = set()
			no_common_nodes = True
			
			for word_index in range(len(self.inputWords)): # ADDED
				currentWord = self.inputWords[word_index]
				for other_w_index in range(word_index+1, len(self.inputWords)):
					#raw trees are the subtrees extracted with breadth first search
					for i in range(len(self.raw_trees)):
						tree_1 = self.raw_trees[i]
						for k in range(i+1, len(self.raw_trees)):
							tree_2 = self.raw_trees[k]
							# no comparison of tree with itself
							min_distance = 6 # at the beginning, this is the maximum distance
							chosen_candidates = []
							for node in tree_1.nodes:
								if node.name in currentWord.synsets and node.name in self.inputWords[other_w_index]:
									if node in tree_2.nodes:
										no_common_nodes = False
										tree_1_root = tree_1.nodes[0]
										tree_2_root = tree_2.nodes[0]
										
										node_2 = tree_2[tree_2.index(node)]
										distanceToRoot12 = node.tree_dictionary[tree_1_root][1] + node_2.tree_dictionary[tree_2_root][1]
										if distanceToRoot12 <= min_distance:
											chosen_candidates[0] = node
											chosen_candidates[1] = node_2
											min_distance = distanceToRoot12
							node = chosen_canditates[0]
							node_2 = chosen_candidates[1]
							# process node from tree 1
							for relevant_node in node.tree_dictionary.keys():
								#saved the common node and its root from tree_2
								relevant_nodes.update(relevant_node)
								length = node.tree_dictionary[tree_1_root][1] # path length
								if length == 2:
									path_to_root_node = node.tree_dictionary[tree_1_root][0][0]
									relevant_nodes.update(path_to_root_node)
								elif length == 3:
									path_to_root_node = node.tree_dictionary[tree_1_root][0][0]
									relevant_nodes.update(path_to_root_node)
									path_to_root_node_2 = path_to_root_node.tree_dictionary[tree_1_root][0][0]
									relevant_nodes.update(path_to_root_node_2)
								
							#same node is also in tree 2
							
							for relevant_node_2 in node_2.tree_dictionary.keys():
								relevant_nodes.update(relevant_node_2)
								length_2 = node_2.tree_dictionary[tree_2_root][1] # path length
								if length_2 == 2:
									path_to_root_node_21 = node_2.tree_dictionary[tree_2_root][0][0]
									relevant_nodes.update(path_to_root_node_21)
								elif length_2 == 3:
									path_to_root_node_21 = node_2.tree_dictionary[tree_2_root][0][0]
									relevant_nodes.update(path_to_root_node_21)
									path_to_root_node_3 = path_to_root_node_21.tree_dictionary[tree_2_root][0][0]
									relevant_nodes.update(path_to_root_node_3)
				
			if no_common_nodes == True:
				for tree in self.raw_trees:
					relevant_nodes.update(tree.nodes)
			graph = Graph(self.inputWords, list(relevant_nodes), d)	
			return graph
					

if __name__ == "__main__":
	#mock of word objects as input
	#word1 = Word("athletic_game")
	#word2 = Word("cat")
	word3 = "kin"
	listOfAnimals = [word3] # reference to object
	wordsearcher = WordNetSearcher(listOfAnimals)
	
	WordNetSearcher.readIndexFiles()
	WordNetSearcher.readDataFiles()
	wordsearcher.createTrees()
	graph = wordsearcher.constructGraph2(0.85)
	for node in graph.nodes:
		print node.name
		#for node in tree.nodes:
		#	print node.name
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