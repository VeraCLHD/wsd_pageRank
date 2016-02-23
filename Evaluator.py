import WordNetSearcher
import OntoNodesSentenceExtractor

class Evaluator:
	def __init__(self, graph_construction_style, measure_type, d=0.8):
        if measure_type in ["PR", "KPP", "iD", "BWN", "MF"]:
            self.measure_type = measure_type
        else:
            sys.stderr.write('illegal measure_type. has to be "PR", "KPP", "iD", "BWN" or "MF"')
        if type(d) == float or int:
            self.d = d
        else:
            sys.stderr.write('illegal type for d. has to be float or int')
        if self.graph_construction_style in ["normal", "full"]:
            self.graph_construction_style = graph_construction_style
        else:
            sys.stderr.write('illegal type for graph_construction_style. has to be "normal" or "full"')
        self.true_positives = 0
        self.false_positives = 0
        self.false_negatives = 0
        self.non_recognized = 0
        self.sum = 0
        
        self.precision = 0
        self.recall = 0
        self.accuracy = 0
        self.f_measure = 0
        self.specifity = 0
        self.AUC = 0 #area under the curve
            

        
        
    def evaluate(self):
        o = ontoNodesSentenceExtractor()
        e = Evaluator("normal", "PR", 0.8)
        while sentence not []:
            sentence = ontoNodesSentenceExtractor.get_next_sentence()
            words = ontoNodesSentenceExtractor.sentenceToWords()
            g = WordNetSearcher.createGraph(words)
            if e.measure_type = "PR":
                g.calculatePageRank(g.d)
            if e.measure_type = "KPP":
                g.calculateKPP()
            if e.measure_type = "iD":
                g.calculateInDegree()
            if e.measure_type = "BWN":
                g.calculateKPP()
                g.calculateBetweenness()
            if e.measure_type = "MF":
                g.calculateMaximumFlow()
            results = g.getResults(measure_type)
            if len(results)!=len(sentence):
                sys.stderr.write("fatal error: gold and auto sentences don't have same length")
            else: #fill evaluation
                for word in results:
                    if word[0]!=sentence[0]:
                        sys.stderr.write('fatal error: words not at the same place in gold and auto sentence')
                    else:
                        self.sum += 1 #all words
                        if word[1] == sentence[1]: #correctly classified
                            self.true_positives += 1
                        else:
                            if word[1] == "": #dead word -> not classified
                                self.false_negatives += 1
                                self.non_recognized += 1
                            else: #wrongly classified
                                self.false_negatives += 1
                                self.false_positives += 1
        self.accuracy = float(self.true_positives + self.true_negatives)/self.all
        self.micro_precision = float(self.true_positives)/(self.true_positives + self.false_positives)
        self.micro_recall = float(self.true_positives)/(self.true_positives+self.false_negatives)
        self.micro_f_measure = 2*float(self.precision*self.recall)/(self.precision+self.recall)
        
        finals = [self.accuracy, self.micro_precision, self.micro_recall, self.micro_f_measure, self.non_recognized]
        print "Results in order: Accuracy, Precision, Recall, F-Measure, Non-recognized"
        for measure in finals:
            print measure