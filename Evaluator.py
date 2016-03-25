import WordNetSearcher
import OntoNodesSentenceExtractor
import sys

class Evaluator:
    def __init__(self, graph_construction_style, measure_type, d=0.85):
        if measure_type in ["PR", "PPR", "KPP", "iD", "BWN", "MF"]:
            self.measure_type = measure_type
        else:
            sys.stderr.write('illegal measure_type. has to be "PR", "PPR", "KPP", "iD", "BWN" or "MF"')
        if type(d) == float or int:
            self.d = d
        else:
            sys.stderr.write('illegal type for d. has to be float or int')
        if graph_construction_style in ["normal", "full"]:
            self.graph_construction_style = graph_construction_style
        else:
            sys.stderr.write('illegal type for graph_construction_style. has to be "normal" or "full"')
        self.true_positives = 0
        #self.true_negatives = 0
        self.false_positives = 0
        self.false_negatives = 0
        self.non_recognized = 0
        self.sum = 0
        
        self.micro_precision = 0
        self.micro_recall = 0
        self.f_measure = 0
            

        
    @staticmethod    
    def evaluate(mode, measureType, onto):
        e = Evaluator(mode, measureType)

        sentence = True

        while sentence:
            sentence = onto.getNextSentence()
            if len(sentence) > 0:
                # print sentence
                words = onto.sentenceToWords(sentence)

                wordsearcher = WordNetSearcher.WordNetSearcher(words)

                wordsearcher.createTrees()
                g = wordsearcher.constructGraph(0.85)
                
                if e.measure_type == "PR":
                    g.calculatePageRank(g.d)
                if e.measure_type == "PPR":
                    g.calculatePersonalPageRank(g.d)
                if e.measure_type == "KPP":
                    g.calculateKPP()
                if e.measure_type == "iD":
                    g.calculateInDegree()
                if e.measure_type == "BWN":
                    g.calculateKPP()
                    g.calculateBetweenness()
                if e.measure_type == "MF":
                    g.calculateMaximumFlow()
                if e.measure_type == "ALL":
                    g.calculatePageRank(g.d)
                    g.calculatePersonalPageRank(g.d)
                    g.calculateKPP()
                    g.calculateInDegree()
                    g.calculateBetweenness()
                    g.calculateMaximumFlow()
                results = g.getResults(e.measure_type)
                if len(results)!=len(sentence):
                    sys.stderr.write("fatal error: gold and auto sentences don't have same length")
                else: #fill evaluation
                    for sentence_iterator in range(len(sentence)):
                        word = results[sentence_iterator]
                        sent = sentence[sentence_iterator]
                        if word[0] != sent[0]:
                            sys.stderr.write('fatal error: words not at the same place in gold and auto sentence')
                        else:
                            e.sum += 1 #all words
                            if word[1] in sent[1]: #correctly classified
                                e.true_positives += 1
                            elif sent[1] == []:
                                e.true_positives += 1
                            else:
                                if word[1] == "": #dead word -> not classified
                                    e.false_negatives += 1
                                    e.non_recognized += 1
                                else: #wrongly classified
                                    e.false_negatives += 1
                                    e.false_positives += 1
        e.micro_precision = float(e.true_positives)/(e.true_positives + e.false_positives)
        e.micro_recall = float(e.true_positives)/(e.true_positives+e.false_negatives)
        e.micro_f_measure = 2*float(e.micro_precision*e.micro_recall)/(e.micro_precision+e.micro_recall)
        
        finals = [e.micro_precision, e.micro_recall, e.micro_f_measure, e.non_recognized]
        print "Results in order: Precision, Recall, F-Measure, Non-recognized"
        for measure in finals:
            print measure