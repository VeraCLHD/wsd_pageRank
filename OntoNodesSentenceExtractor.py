import Word

class OntoNodesSentenceExtractor:
    def __init__(self, data):
        
        self.processed_corpus = data.returnProcessed()
        self.counter = 0
    
    def getNextSentence(self):
        #print len(self.processed_corpus)
        if self.counter < len(self.processed_corpus):
            dummy_sentence = self.processed_corpus[self.counter]
            self.counter += 1
            #print dummy_sentence
            return dummy_sentence
        else:
            dummy_sentence = []
            self.counter = -1
            #print dummy_sentence
            return dummy_sentence
        #stopWords rauswerfen
        #output: [[word1, [wordNet_sense1]], [word2, [wordNet_sense2]], ...]
        #words sind hier einfach strings, keine objekte der klasse Word
        #bei fehlenden bedeutungen ist die ausgegebene bedeutung ein leerer string
       
    @staticmethod
    def getListFromString(string):
        string = string[1:-1] #remove outer brackets
        first_iteration = OntoNodesSentenceExtractor.splitList(string)
        for sub_list in first_iteration:
            sub_list[0] = OntoNodesSentenceExtractor.splitList(sub_list[0])
        #print first_iteration[0]
        return first_iteration
        
        
    @staticmethod
    def splitList(substring):  
        outerList = []
        inList = False
        start_of_sublist = None
        count_brackets = -1
        for iter in range(len(substring)):
            if inList == False:
                if substring[iter] == "[":
                    start_of_sublist = iter
                    inList = True
            else:
                if substring[iter] == "[":
                    count_brackets -= 1
                if substring[iter] == "]": #end of sublist
                    count_brackets += 1
                    if count_brackets == 0:
                        outerList.append([substring[start_of_sublist+1:iter]])
        return outerList
                
        
    def sentenceToWords(self, sentence):
        dummy_sentence = []
        for a in range(len(sentence)):
            dummy_list = sentence[a]
            dummy_sentence.append(dummy_list[0])
        return dummy_sentence
            
        #input: sentence wie aus get_next_sentence
        #output: [word1, word2, ...]
