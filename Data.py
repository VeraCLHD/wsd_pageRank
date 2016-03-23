import DataReader
import glob
import os

class Data(object):
	def __init__(self):
		
		# Creating dummies to fill in
		self.rawOntoNodes_data = []
		self.rawIndex_data = []
		self.rawFunctionWord_data = []
		self.rawTranslator_data = []
		
		self.processed_sentences = []

	# HAS TO <ADD> FIRST
	def returnRawOnData(self):
		return self.rawOntoNodes_data
	def returnRawInData(self):
		return self.rawIndex_data
	def returnRawFwData(self):
		return self.rawFunctionWord_data
	def returnRawTlData(self):
		return self.rawTranslator_data
	
	# HAS TO <PROCESS> FIRST
	def returnProcessed(self):
		return self.processed_sentences
	
	
	# Collect Data from files
	def addData(self, location, type):
		dummy_reader = DataReader.Reader(location, type)
		dummy_reader.readFile()
		dummy_reader.processContent()
		if type == "ON":
			self.rawOntoNodes_data = dummy_reader.procontent
		if type == "IN":
			for a in range(len(dummy_reader.procontent)):
				self.rawIndex_data.append(dummy_reader.procontent[a])
		if type == "FW":
			for a in range(len(dummy_reader.procontent)):
				self.rawFunctionWord_data.append(dummy_reader.procontent[a])
		if type == "TL":
			for a in range(len(dummy_reader.procontent)):
				self.rawTranslator_data.append(dummy_reader.procontent[a])
		
			
	
	def addFolder(self, location, format, type):
		for filename in glob.glob(os.path.join(location, format)):
			self.addData(filename, type)
				
			
	# Process the rawData to useful one
	def processData_to_sentences(self):
		dummy_sentence = []
		errors = 0
		# Look at the corpus
		for a in range(len(self.rawOntoNodes_data)):
			# Look for sentences
			if a == 0 or self.rawOntoNodes_data[a].word_in_sentence > self.rawOntoNodes_data[a-1].word_in_sentence:
				dummy_word_and_senses = []
				# Kick function words
				if self.rawOntoNodes_data[a].word not in self.rawFunctionWord_data:
					dummy_word_and_senses.append(self.rawOntoNodes_data[a].word)
					dummy_sense = []
					dummy_sense_untranslated = []
					#Check for translator
					if self.rawOntoNodes_data[a].sense != 0:
						for b in range(len(self.rawTranslator_data)):
							if self.rawTranslator_data[b].word == self.rawOntoNodes_data[a].word and self.rawTranslator_data[b].wordtype == self.rawOntoNodes_data[a].wordtype:
								# Get the first part of translation	
								try:
									dummy_sense_untranslated = self.rawTranslator_data[b].senselists[self.rawOntoNodes_data[a].sense-1]
								except IndexError:
									dummy_sense_untranslated = []
									errors += 1
								for c in range(len(self.rawIndex_data)):
									# Search for word in index
									if self.rawIndex_data[c].word == self.rawOntoNodes_data[a].word and self.rawIndex_data[c].wordtype == self.rawOntoNodes_data[a].wordtype:
										# Does it have a double meaning?
										for d in range(len(dummy_sense_untranslated)):
											try:
												dummy_sense.append(self.rawIndex_data[c].senselist[dummy_sense_untranslated[d]-1])
											# It is only 1 off anyway.
											except IndexError:
												dummy_sense.append(self.rawIndex_data[c].senselist[dummy_sense_untranslated[d]-2]
												errors += 1
							
					# Clear dummies
					dummy_word_and_senses.append(dummy_sense)
					dummy_sentence.append(dummy_word_and_senses)				
			else:
				# Add the completed sentence
				self.processed_sentences.append(dummy_sentence)
				# Clear dummies
				dummy_sentence = []
				dummy_word_and_senses = []
				# Kick function words
				if self.rawOntoNodes_data[a].word not in self.rawFunctionWord_data:
					dummy_word_and_senses.append(self.rawOntoNodes_data[a].word)
					dummy_sense = []
					# Check index data
					for b in range(len(self.rawIndex_data)):
						# Find word in index data
						if self.rawIndex_data[b].word == self.rawOntoNodes_data[a].word and self.rawIndex_data[b].wordtype == self.rawOntoNodes_data[a].wordtype:
							# Double meanings?
							if self.rawOntoNodes_data[a].sense == 0:
								dummy_sense.append(self.rawIndex_data[b].senselist[(self.rawOntoNodes_data[a].sense)])
							else:
								dummy_sense.append(self.rawIndex_data[b].senselist[(self.rawOntoNodes_data[a].sense-1)])

					# Clear dummies		
					dummy_word_and_senses.append(dummy_sense)
					dummy_sentence.append(dummy_word_and_senses)
		# Add final sentence
		self.processed_sentences.append(dummy_sentence)
		print errors

if __name__ == "__main__":
	
	# WARNING		WARNING		WARNING
	# WARNING	absolute path!	WARNING
	# WARNING		WARNING		WARNING
	
	Data1 = Data()
	
	print
	print "SETUP STARTS"
	print
	print "part1"
	Data1.addData("D:/TEST/Corpus/big_test.txt","ON")
	print "part2"
	Data1.addData("D:/TEST/Index/index.adj","IN")
	Data1.addData("D:/TEST/Index/index.adv","IN")
	Data1.addData("D:/TEST/Index/index.noun","IN")
	Data1.addData("D:/TEST/Index/index.verb","IN")
	print "part3"
	Data1.addFolder("D:/TEST/FunctionWords/","*.txt","FW")
	print "part4"
	Data1.addFolder("D:/TEST/Translation/","*.xml","TL")
	print
	print "SETUP DONE"
	print 
	print "part1"
	#print(Data1.returnRawOnData())
	print
	print "part2"
	#print(Data1.returnRawInData())
	print
	print "part3"
	#print(Data1.returnRawFwData())
	print
	print "part4"
	#print(Data1.returnRawTlData())
	print
	print "PROCESS START"
	print 
	Data1.processData_to_sentences()
	print 
	print
	print(Data1.returnProcessed())
	print
	print "DONE"

	 