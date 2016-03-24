import Lemma
import Translation
import Translator
import os

class Reader():
    def __init__(self, file, type):
        
        # Path to the file -> STR
        self.filename = str(file)
        # Type of file (e.x. ON for OntoNotes, FW for FilterWords etc) -> STR
        self.filetype = str(type)
        # Create dummies to fill later on
        self.rawcontent = []
        self.procontent = []
        
        self.case1 = 0
        self.case2 = 0
        self.case3 = 0
        self.case4 = 0
        self.case5 = 0
        self.case6 = 0
        self.case7 = 0
        self.case8 = 0
        self.case9 = 0
        self.case10 = 0
    
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
        
        
        
    # Actions
    
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
                if self.rawcontent[a] != "" and "#begin" not in self.rawcontent[a] and "#end" not in self.rawcontent[a]:
                    splitLine = self.rawcontent[a].split()
                    # Pick out the juicy bits
                    dummy_lemma = Lemma.Lemma(int(splitLine[1]), int(splitLine[2]), str(splitLine[3]).lower(), str(splitLine[4]), str(splitLine[6]).lower(), str(splitLine[8]))
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
        if self.filetype == "FW":
            # Kick the useless first 25 entries
            for a in range(25,len(self.rawcontent)):
                # Kick useless empty lines
                if self.rawcontent[a] != "" and "//" not in self.rawcontent[a]:
                    # Check for multiple examples
                    splitLine = self.rawcontent[a].split(", ")
                    dummy_functionWords = []
                    # Take all examples
                    for b in range(len(splitLine)):
                        # Kick constructions of multiple words
                        if " " not in splitLine[b]:
                            self.procontent.append(splitLine[b])
        if self.filetype == "TL":
            dummy_senselists = []
            dummy_switch = False
            # Get the info from filename back
            dir = os.path.realpath(__file__)
            dummy_string = self.filename.replace("\\".join(dir.split("\\")[:-1])+"\\Translation\\","").replace(".xml","")
            dummy_word_and_type = dummy_string.split("-")

            for a in range(0,len(self.rawcontent)):
                # Look out for juicy bits
                #
                # The following part is NSFW
                #
                # This is a dummy in case the file just wanted to put info in a new line
                
                if dummy_switch == True:
                    
                    dummy_string = self.rawcontent[a]
                    # This is in case the file wanted to add an additional empty line
                    if dummy_string != "":
                        # Yes, there are files with additional info instead
                        if "<wn lemma" not in dummy_string and dummy_string != "-" and "<omega" not in dummy_string:
                            splitLine = dummy_string.split(" ")
                            dummy_list = []
                            for b in range(len(splitLine)):
                                try:
                                    dummy_list.append(int(splitLine[b]))
                                # It is 3am , now I stop to care and start to botch
                                except ValueError:
                                    dummy_splitLine = splitLine[0].split(",")
                                    dummy_list.append(int(dummy_splitLine[b]))
                            dummy_senselists.append(dummy_list)
                            #print dummy_senselists
                        elif dummy_string != "-":
                            dummy_senselists.append([0])
                            #print dummy_senselists
                        # This is not the normal format either    
                        else:
                            # Kick useless stuff
                            dummy_splitLine1 = dummy_string.split("version=\"3.0\">")
                            dummy_splitLine2 = dummy_splitLine1[-1].split("</wn>")
                            splitLine = dummy_splitLine2[0].split(",")
                            if splitLine[0] != "" and splitLine[0] != "-":
                                dummy_list = []
                                for b in range(len(splitLine)):
                                        dummy_list.append(int(splitLine[b]))
                                dummy_senselists.append(dummy_list)
                                #print dummy_senselists
                        ###    elif splitLine[0] == "-":
                        ###        dummy_senselists.append([0])
                            else: 
                                dummy_senselists.append([0])
                                #print dummy_senselists
                        dummy_switch = False
                # That is the normal format I would say. Not sure though.
                if "<wn version=\"3.0\">" in self.rawcontent[a]:
                    # Kick the useless stuff around juicy bit
                    dummy_string = self.rawcontent[a].replace("<wn version=\"3.0\">","").replace("</wn>","").replace("<omega/>","")
                    splitLine = dummy_string.split(",")
                    if splitLine[0] != "" and splitLine[0] != "NM":
                        dummy_list = []
                        for b in range(len(splitLine)):
                            if "." in splitLine[b]:
                                dummy_list.append(int(splitLine[b].split(".")[0]))
                            else:
                                dummy_list.append(int(splitLine[b]))
                        dummy_senselists.append(dummy_list)
                        #print dummy_senselists
                    elif splitLine[0] == "NM":
                        dummy_senselists.append([0])
                        #print dummy_senselists
                    else:
                        dummy_switch = True
                if "<wn version=\"1.7\">" in self.rawcontent[a]:
                    # Blub
                    dummy_string = self.rawcontent[a].replace("<wn version=\"1.7\">","").replace("</wn>","").replace("<omega/>","")
                    splitLine = dummy_string.split(",")
                    if splitLine[0] != "" and splitLine[0] != "NM" and splitLine[0] != "?":
                        dummy_list = []
                        for b in range(len(splitLine)):
                            if "." in splitLine[b]:
                                dummy_list.append(int(splitLine[b].split(".")[0]))
                            else:
                                dummy_list.append(int(splitLine[b]))
                        dummy_senselists.append(dummy_list)
                        #print dummy_senselists
                    elif splitLine[0] == "NM" or splitLine[0] == "?" or splitLine[0] == "-":
                        dummy_senselists.append([0])
                        #print dummy_senselists
                    else:
                        dummy_switch = True
                # By now, anything could happen in these lines
                if "<wn version=\"2.0\">" in self.rawcontent[a] and "</wn>" in self.rawcontent[a]:
                    dummy_list = []
                    dummy_string = self.rawcontent[a]
                    dummy_splitLine1 = dummy_string.split("version=\"2.0\">")
                    dummy_splitLine2 = dummy_splitLine1[-1].split("</wn>")
                    dummy_splitLine3 = dummy_splitLine2[0].split(",")
                    splitLine = dummy_splitLine3[0].split(" ")
                    if splitLine[0] != "" and splitLine[0] != "-" and splitLine[0] != "Placeholder":
                        dummy_list = []
                        for b in range(len(splitLine)):
                            try:
                                dummy_list.append(int(splitLine[b]))
                            except ValueError:
                                print self.rawcontent[a]
                                print self.filename
                        dummy_senselists.append(dummy_list)
                        #print dummy_senselists
                    else: 
                        dummy_senselists.append([0])
                        #print dummy_senselists
                if "<wn version=\"2.0\">" in self.rawcontent[a] and "</wn>" not in self.rawcontent[a]:
                    dummy_switch = True
            dummy_translator = Translator.Translator(dummy_word_and_type[0],dummy_word_and_type[1],dummy_senselists)
            self.procontent.append(dummy_translator)
            
            
            

            
    
    # >>>FOR TESTING ONLY<<<
    def translateProcontent(self):
        if self.filetype == "ON":
            for a in range(len(self.procontent)):
                print(self.procontent[a].returnLemma())
        if self.filetype == "IN":
            for a in range(len(self.procontent)):
                print(self.procontent[a].returnTranslation())    
        if self.filetype == "TL":
            for a in range(len(self.procontent)):
                print(self.procontent[a].returnTranslator())

if __name__ == "__main__":
    
    # WARNING        WARNING        WARNING
    # WARNING    absolute path!    WARNING
    # WARNING        WARNING        WARNING
    
    #reader1 = Reader("D:/TEST/Corpus/reader_test.txt","ON")
    #reader2 = Reader("D:/TEST/Index/index.adj","IN")
    #reader3 = Reader("D:/TEST/FunctionWords/EnglishPrepositions.txt","FW")
    reader4 = Reader("D:/TEST/Translation/add-v.xml","TL")
    
    # print
    # print "SETUP STARTS"
    # print
    # print "Location:"
    # print(reader1.returnFilename())
    # print "Type:"
    # print(reader1.returnFiletype())
    # print "(Emtpy) Raw:"
    # print(reader1.returnRawcontent())
    # print "(Empty) pro:"
    # print(reader1.returnProcontent())
    # print
    # print "READING STARTS"
    # print
    # reader1.readFile()
    # print "New raw:"
    # print(reader1.returnRawcontent())
    # print
    # print "PROCESSING STARTS"
    # print
    # reader1.processContent()
    # print "New pro:"
    # print(reader1.returnProcontent())
    # print
    # print "<Translating>"
    # reader1.translateProcontent()

    # print
    # print "SETUP STARTS"
    # print
    # print "Location:"
    # print(reader2.returnFilename())
    # print "Type:"
    # print(reader2.returnFiletype())
    # print "(Emtpy) Rrw:"
    # print(reader2.returnRawcontent())
    # print "(Empty) pro:"
    # print(reader2.returnProcontent())
    # print
    # print "READING STARTS"
    # print
    # reader2.readFile()
    # print "New raw:"
    # print(reader2.returnRawcontent())
    # print
    # print "PROCESSING STARTS"
    # print
    # reader2.processContent()
    # print "New pro:"
    # print(reader2.returnProcontent())
    # print
    # print "<Translating>"
    # reader2.translateProcontent()
    
    # print
    # print "SETUP STARTS"
    # print
    # print "Location:"
    # print(reader3.returnFilename())
    # print "Type:"
    # print(reader3.returnFiletype())
    # print "(Emtpy) Rrw:"
    # print(reader3.returnRawcontent())
    # print "(Empty) pro:"
    # print(reader3.returnProcontent())
    # print
    # print "READING STARTS"
    # print
    # reader3.readFile()
    # print "New raw:"
    # print(reader3.returnRawcontent())
    # print
    # print "PROCESSING STARTS"
    # print
    # reader3.processContent()
    # print "New pro:"
    # print(reader3.returnProcontent())
    # print
    
    print
    print "SETUP STARTS"
    print
    print "Location:"
    print(reader4.returnFilename())
    print "Type:"
    print(reader4.returnFiletype())
    # print "(Emtpy) Rrw:"
    # print(reader4.returnRawcontent())
    # print "(Empty) pro:"
    # print(reader4.returnProcontent())
    print
    print "READING STARTS"
    print
    reader4.readFile()
    print "New raw:"
    print(reader4.returnRawcontent())
    print
    print "PROCESSING STARTS"
    print
    reader4.processContent()
    print "New pro:"
    print(reader4.returnProcontent())
    print
    print "<Translating>"
    reader4.translateProcontent()