import Lemma
import Translation

class Reader():
	def __init__(self, file, type):
		
		# Path to the file -> STR
		self.filename = str(file)
		# Type of file (e.x. ON for OntoNotes, FW for FilterWords etc) -> STR
		self.filetype = str(type)
		# Create dummies to fill later on
		self.rawcontent = []
		self.procontent = []
	
	#return value stuff
	def returnFilename(self):
		# STR
		return self.filename
	
	def returnFiletype(self):
		# STR
		return self.filetype
	
	# HAS TO <READ> FIRST
	def returnRawcontent(self):
		# List[String]
		return self.rawcontent
	
	# HAS TO <PROCESS> FIRST
	def returnProcontent(self):
		# List[Lemma]
		return self.procontent
	
	# Read ALL the data from a file
	def readFile(self):
		# Closes automatically
		with open(self.filename) as f:
			self.rawcontent = [line.strip(' \t\n\r') for line in f]

			
	# Process the raw data into only useful information
	def processContent(self):
		if self.filetype == "ON":
			# Kick the useless first entry
			for a in range(1,len(self.rawcontent)):
				# Kick useless empty lines
				if self.rawcontent[a] != "":
					splitLine = self.rawcontent[a].split()
					# Pick out the juicy bits
					dummy_lemma = Lemma.Lemma(int(splitLine[1]), int(splitLine[2]), str(splitLine[3]), str(splitLine[4]), str(splitLine[6]), str(splitLine[8]))
					self.procontent.append(dummy_lemma)
		if self.filetype == "IN":
			# Kick the useless first 29 entries
			for a in range(29,len(self.rawcontent)):
				# Kick useless empty lines
				if self.rawcontent[a] != "":
					splitLine = self.rawcontent[a].split()
					# Pick out the juicy bits
					dummy_list_of_senses = []
					# Check for multiple senses
					for b in range(6,len(splitLine)):
						if len(splitLine[b]) > 3:
							dummy_list_of_senses.append(splitLine[b])
					# Putting juicy bits together
					dummy_translation = Translation.Translation(str(splitLine[0]), str(splitLine[1]), dummy_list_of_senses)
					self.procontent.append(dummy_translation)
					
				
	
	# >>>FOR TESTING ONLY<<<
	def translateProcontent(self):
		if self.filetype == "ON":
			for a in range(len(self.procontent)):
				print(self.procontent[a].returnLemma())
		if self.filetype == "IN":
			for a in range(len(self.procontent)):
				print(self.procontent[a].returnTranslation())	

if __name__ == "__main__":
	
	# WARNING		WARNING		WARNING
	# WARNING	absolute path!	WARNING
	# WARNING		WARNING		WARNING
	
	reader1 = Reader("D:/TEST/test.txt","ON")
	reader2 = Reader("D:/TEST/index.adj","IN")
	
#	print
#	print "SETUP STARTS"
#	print
#	print "Location:"
#	print(reader1.returnFilename())
#	print "Type:"
#	print(reader1.returnFiletype())
#	print "(Emtpy) Rrw:"
#	print(reader1.returnRawcontent())
#	print "(Empty) pro:"
#	print(reader1.returnProcontent())
#	print
#	print "READING STARTS"
#	print
#	reader1.readFile()
#	print "New raw:"
#	print(reader1.returnRawcontent())
#	print
#	print "PROCESSING STARTS"
#	print
#	reader1.processContent()
#	print "New pro:"
#	print(reader1.returnProcontent())
#	print
#	print "<Translating>"
#	reader1.translateProcontent()

#	print
#	print "SETUP STARTS"
#	print
#	print "Location:"
#	print(reader2.returnFilename())
#	print "Type:"
#	print(reader2.returnFiletype())
#	print "(Emtpy) Rrw:"
#	print(reader2.returnRawcontent())
#	print "(Empty) pro:"
#	print(reader2.returnProcontent())
#	print
#	print "READING STARTS"
#	print
#	reader2.readFile()
#	print "New raw:"
#	print(reader2.returnRawcontent())
#	print
#	print "PROCESSING STARTS"
#	print
#	reader2.processContent()
#	print "New pro:"
#	print(reader2.returnProcontent())
#	print
#	print "<Translating>"
#	reader2.translateProcontent()
	