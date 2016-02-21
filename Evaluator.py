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

            

        
        
    def evaluate(self):
        o = ontoNodesSentenceExtractor()
        while sentence not []:
            sentence = ontoNodesSentenceExtractor.get_next_sentence()
            words = ontoNodesSentenceExtractor.sentenceToWords()
            g = WordNetSearcher.createGraph(words)
            if measure_type = "PR":
                g.calculatePageRank(g.d)
            if measure_type = "KPP":
                g.calculateKPP()
            if measure_type = "iD":
                g.calculateInDegree()
            if measure_type = "BWN":
                g.calculateKPP()
                g.calculateBetweenness()
            if measure_type = "MF":
                g.calculateMaximumFlow()
            results = g.getResults(measure_type)
            
            