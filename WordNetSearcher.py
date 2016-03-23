#!/usr/bin/python
# Python 2.7

import time
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
        self.inputWords = [] #words of one input sentence
        for word in inputWords:
            self.inputWords.append(Word(word))
        self.raw_trees = [] #contains all subtrees
        self.deadSentence = False
        self.nodes = set() #this contains all nodes that are in all subtrees
        self.graph_nodes = set() #here the final graph is created
        self.root_nodes = set() #this is the set of all root nodes
        self.combinations = []

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
        dict = WordNetSearcher.indexDictionary
        indexOfFirstSynset = 3 + int(pnt_count) + 3 # pnt_count is at index 3 + relations + 2 for synset count and target_synset count + 1 -> first index of synset
        synsets = set(lineAsList[indexOfFirstSynset:len(lineAsList)])
        if lemma in dict:
            dict[lemma].update(synsets)
        else:
            dict.setdefault(lemma, synsets)
    
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
        dict = WordNetSearcher.dataDictionary
        if synset in dict:
            dict[synset].update(semRelations)
        else:
            dict.setdefault(synset, semRelations)

    def getMeaningsForWord(self, word):
        wordfoundInWordnet = False
        lemma = word.name
        dict = WordNetSearcher.indexDictionary
        if lemma in dict:
            for synsetString in dict[lemma]:
                newNode = Node.createNode(synsetString)
                word.synsets.add(newNode)
                self.root_nodes.add(newNode)
                self.nodes.add(newNode)
        else:
            word.DeadWord = True
            sys.stderr.write("This word is empty or was not found in WordNet 2.1")
    
    def createTree(self, wurzel):
        print "createTree"
        queue = [wurzel]
        this_iteration = []
        results = [wurzel]
        iterator = 0
        while iterator < 3:
            iterator += 1
            for node in queue:
                for neighbour in WordNetSearcher.dataDictionary[node.name]:
                    neighbour_node = Node.createNode(neighbour)
                    self.nodes.add(neighbour_node)
                    neighbour_node.neighbours = WordNetSearcher.dataDictionary[neighbour]
                    if not neighbour_node in results:
                        results.append(neighbour_node)
                        this_iteration.append(neighbour_node)
                        neighbour_node.tree_dictionary[wurzel] = [[node], iterator]
                    else:
                        if neighbour_node.tree_dictionary[wurzel][1] == iterator: #diese vier zeilen braucht man um ggf das tree_dictionary um node zu erweitern
                            neighbour_node.tree_dictionary[wurzel][0].append(node)
            queue = this_iteration
            this_iteration = []
        subtree = Tree(results)
        self.raw_trees.append(subtree)
        
                
    def createTrees(self):
        # should create a tree for each synset
        #nodes = []
        for word in self.inputWords:
            wordString = word.name
            if not word.deadWord:
                self.getMeaningsForWord(word)
                synsetsForWord = word.synsets
                for synset in synsetsForWord:
                    root_node = Node.createNode(synset)
                    self.root_nodes.add(root_node)
                    root_node.neighbours = WordNetSearcher.dataDictionary[synset.name]
                    self.createTree(root_node)
    
    
    def constructGraph(self, d):
        print "construct graph"
        count = 0
        print self.root_nodes
        for node in self.nodes: #search for all nodes that will belong to the graph
            if len(node.tree_dictionary.keys())>2: #this node only creates a new path if it is close enough to at least two root_nodes
                self.graph_nodes.add(node) #the node itself is added to graph
                dicti = list(node.tree_dictionary.keys())
                dicti.remove(node)
                for key_iter1 in range(1, len(dicti)):
                    for key_iter2 in range(key_iter1+1, len(dicti)):
                        key1 = dicti[key_iter1]
                        key2 = dicti[key_iter2]
                        print node
                        print key1, key2
                        first_word = None
                        relevant_synsets = False
                        for word in self.inputWords: #all that is coming in the next 15 lines is to check if two synsets belong to the same word. if that is the case, their path is not added to the graph
                            for synset in word.synsets:
                                if synset == key1:
                                    if first_word == None:
                                        first_word = word
                                        break
                                    else:
                                        relevant_synsets = True
                        if relevant_synsets == False:
                            if not key2 in first_word.synsets:
                                for word in self.inputWords:
                                    if word != first_word:
                                        for synset in word.synsets:
                                            if synset == key2:
                                                relevant_synsets = True
                            else:
                                relevant_synsets = True
                        
                        if relevant_synsets == True:
                            if not [key1, key2] in self.combinations:
                                self.combinations.append([key1, key2])
                                #print key1, key2
                                present_node = node
                                while not present_node == key1: #walk to first root, collect the nodes
                                    present_node = present_node.tree_dictionary[key1][0][0]
                                    self.graph_nodes.add(present_node)
                                present_node = node
                                while not present_node == key2: #walk to second node
                                    present_node = present_node.tree_dictionary[key2][0][0]
                                    self.graph_nodes.add(present_node)
                            else:
                                print "yeahyeahyeah"
        for node in self.graph_nodes: #delete all nodes and connections that don't belong to the graph
            neighbours_nodes = list(node.neighbours)
            for sub_node in node.neighbours:
                if sub_node not in self.graph_nodes:
                    neighbours_nodes.remove(sub_node)
            node.neighbours = neighbours_nodes
        graph = Graph(self.inputWords, self.root_nodes, self.graph_nodes, d)
        # for node in graph.node: #delete all neighbours in tree_dicionary that are not in the graph
            # for neighbour in node.tree_dictionary.keys():
                # if neighbour not in self.tree_nodes:
                    # tree_dictionary.pop(neighbour)
        return graph
                                

if __name__ == "__main__":
    print "creating index files"
    WordNetSearcher.readIndexFiles()
    print "creating data files"
    WordNetSearcher.readDataFiles()
    print "starting algorithm"
    listOfAnimals = ["am", "cat", "fish", "tree"] # reference to object
    print "start wordNetSearcher"
    wordsearcher = WordNetSearcher(listOfAnimals)
    wordsearcher.createTrees()
    
    g = wordsearcher.constructGraph(0.85)
    print len(wordsearcher.nodes)
    print len(g.nodes)
    # g.calculatePageRank(g.d)
    # g.calculatePersonalPageRank(g.d)
    g.calculateKPP()
    g.calculateInDegree()
    g.calculateBetweenness()
    # g.calculateMaximumFlow()
    # print "pageRank:"
    # print g.getResults("PR")
    # print "personalized pageRank"
    # print g.getResults("PPR")
    # print "key player:"
    print g.getResults("KPP")
    # print "in-Degree:"
    print g.getResults("iD")
    # print "Betweenness:"
    print g.getResults("BWN")
    # print "Maximum Flow:"
    # print g.getResults("MF")
    
    #graph = wordsearcher.constructGraph2(self.input_words, WordNetSearcher.indexDictionary.keys(), self.dataDictionary.keys(), 0.85) #words, word_nodes, nodes, d
    #for node in graph.nodes:
        #print node.name
        #for node in tree.nodes:
        #    print node.name
    #for synset in WordNetSearcher.indexDictionary[word3.name]:
    #    print "SYNSET: " + synset
    #    print WordNetSearcher.dataDictionary[synset]
    #graph = wordsearcher.createInitialTreeDraft()
    #if graph != None:
    #    for node in graph.nodes:
    #        print node.name
    #        print node.neighbours
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