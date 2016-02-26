import Lemma

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
			for b in range(1,len(self.rawcontent)):
				# Kick useless empty lines
				if self.rawcontent[b] != "":
					splitLine = self.rawcontent[b].split()
					# Pick out the juicy bits
					dummy_lemma = Lemma.Lemma(int(splitLine[1]), int(splitLine[2]), str(splitLine[3]), str(splitLine[4]), str(splitLine[6]), str(splitLine[8]))
					self.procontent.append(dummy_lemma)
	
	# >>>FOR TESTING ONLY<<<
	def translateProcontent(self):
		for a in range(len(self.procontent)):
			print(self.procontent[a].returnLemma())

if __name__ == "__main__":
	
	# WARNING		WARNING		WARNING
	# WARNING	absolute path!	WARNING
	# WARNING		WARNING		WARNING
	
	reader1 = Reader("D:/TEST/wsd_pageRank/reader_test.txt","ON")
	
	print
	print "SETUP STARTS"
	print
	print "Location:"
	print(reader1.returnFilename())
	print "Type:"
	print(reader1.returnFiletype())
	print "(Emtpy) Rrw:"
	print(reader1.returnRawcontent())
	print "(Empty) pro:"
	print(reader1.returnProcontent())
	print
	print "READING STARTS"
	print
	reader1.readFile()
	print "New raw:"
	print(reader1.returnRawcontent())
	print
	print "PROCESSING STARTS"
	print
	reader1.processContent()
	print "New pro:"
	print(reader1.returnProcontent())
	print
	print "<Translating>"
	reader1.translateProcontent()
	