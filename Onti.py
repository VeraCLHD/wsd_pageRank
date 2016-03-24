import WordNetSearcher
import Evaluator
import Data
import os
import OntoNodesSentenceExtractor

# key: word, value: list of synsets from index file
indexDictionary = {}
# key: synset, value: list of related synsets
dataDictionary = {}

if __name__ == "__main__":
    print "creating index files"
    WordNetSearcher.WordNetSearcher.readIndexFiles()
    print "creating data files"
    WordNetSearcher.WordNetSearcher.readDataFiles()
    print "starting algorithm"
    # listOfAnimals = ["fish", "cat"] # reference to object
    # print "start wordNetSearcher"
    # wordsearcher = WordNetSearcher(listOfAnimals)
    # wordsearcher.createTrees()
    
    # g = wordsearcher.constructGraph(0.85)
    # print "root_nodes:"
    # for node in g.root_nodes:
        # print node
    # print len(wordsearcher.nodes)
    # print len(g.nodes)
    # g.calculatePageRank(g.d)
    # g.calculatePersonalPageRank(g.d)
    # g.calculateKPP()
    # g.calculateInDegree()
    # g.calculateBetweenness()
    # g.calculateMaximumFlow()
    # print "pageRank:"
    # print g.getResults("PR")
    # print "personalized pageRank"
    # print g.getResults("PPR")
    # print "key player:"
    # print g.getResults("KPP")
    # print "in-Degree:"
    # print g.getResults("iD")
    # print "Betweenness:"
    # print g.getResults("BWN")
    # print "Maximum Flow:"
    # print g.getResults("MF")
    
    data = Data.Data()
    dir = os.path.realpath(__file__)

    data.addData("\\".join(dir.split("\\")[:-1])+"\\Corpus\\tiny_test.txt","ON")
    #print "corpus done"
    data.addData("\\".join(dir.split("\\")[:-1])+"\\Index\\index.adj","IN")
    data.addData("\\".join(dir.split("\\")[:-1])+"\\Index\\index.adv","IN")
    data.addData("\\".join(dir.split("\\")[:-1])+"\\Index\\index.noun","IN")
    data.addData("\\".join(dir.split("\\")[:-1])+"\\Index\\index.verb","IN")
    #print "index done"
    data.addFolder("\\".join(dir.split("\\")[:-1])+"\\FunctionWords\\","*.txt","FW")
    #print "functions done"
    data.addFolder("\\".join(dir.split("\\")[:-1])+"\\Translation\\","*.xml","TL")
    #print "trans done"
    
    data.processData_to_sentences()

    #with open("\\".join(dir.split("\\")[:-1])+"\\processedCorpus.txt") as f:
        # process = OntoNodesSentenceExtractor.OntoNodesSentenceExtractor.getListFromString(f.read())
    #print data2
    
    # data2 = process
    ontoNodes = OntoNodesSentenceExtractor.OntoNodesSentenceExtractor(data)
    print "------------ The fun starts here"
    Evaluator.Evaluator.evaluate("normal","PR", ontoNodes)
    Evaluator.Evaluator.evaluate("normal","PPR", ontoNodes)
    Evaluator.Evaluator.evaluate("normal","KPP", ontoNodes)
    Evaluator.Evaluator.evaluate("normal","iD", ontoNodes)
    Evaluator.Evaluator.evaluate("normal","BWN", ontoNodes)
    Evaluator.Evaluator.evaluate("normal","MF", ontoNodes)