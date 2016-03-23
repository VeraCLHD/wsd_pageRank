import Word

class OntoNodesSentenceExtractor:
	def __init__(self, data):
        
		self.processed_corpus = data
		self.counter = -1
    
    def getNextSentence(self):
		if self.counter != len(self.processed_corpus):
			counter += 1
			dummy_sentence =self.processed_corpus[counter]
            return dummy_sentence
		else:
			dummy_sentence = self.processed_corpus[counter]
			counter = -1
            return dummy_sentence
        #stopWords rauswerfen
        #output: [[word1, [wordNet_sense1]], [word2, [wordNet_sense2]], ...]
        #words sind hier einfach strings, keine objekte der klasse Word
        #bei fehlenden bedeutungen ist die ausgegebene bedeutung ein leerer string
        
        
    def sentenceToWords(self, sentence):
		dummy_sentence = []
		for a in range(len(sentence)):
			dummy_list = sentence[a]
			dummy_sentence.append(dummy_list[0])
		return dummy_sentence
			
        #input: sentence wie aus get_next_sentence
        #output: [word1, word2, ...]
