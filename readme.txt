README

Word Sense Disambiguation - Graph measures applied on graphs (WSD - Gag)

Outline

    This project's goal was to devise an algorithm that can determine the word sense of words in a corpus as good as possible by using graph measures.
    Because we thought it was fun we tried to implement multiple kinds - also, pageRank woulndn't feel lonely if it had company.
    The implemented measures are pageRank (as mentioned before), personalized PR, key player problem, in degree, betweenness and maximum float.
    In the first step, all data is taken and used to prepare the annotated corpus for extraction. Then the algorithm does its magic and afterwards the evaluation is rigged, to make us look good.
    
    <Random Bla to fill in later>

Requirements

    Python 2.7 (not provided)
    Wordnet (provided in folder <data>)
    OntoNotes Corpus (provided in folder <Corpus>)
    Data on Function Words & on OntoNotes Annotation (provided in folder <FunctionWords> & <Translation>)
    
Structure and Usage of the single program parts - Preparation

    Data.py
    
        A class structure to hold all information used for preparing the corpus.
    
        Step1:
        addData() & addFolder() -> Add information from target file or directory
        Example:
            addData(location , type_of_file_you_want_to_add)
        >>> Use these to add in Corpus, Index Data, Function Words and Translation Data
        
        Step2:
        processData_to_sentences() -> Use all the stored data to prepare the corpus
        Example:
            processData_to_sentences()
        >>> Use these to prepare the corpus with all other information for usage
        
    
    DataReader.py
    
        A class structure to read any kind of file used in this project and process it according to its type.
    
        readFile()
        Example:
            readFile(file, file_type) -> Store content of file and file_type
        >>> Get content...
        
        processContent() -> Search stored content for useful information and store it
        Example:
            processContent()
        >>> ... and sort out useless stuff
    
    Lemma.py
    
        A class structure to store information about words from the original corpus.

        >>> Only storage
        
    Translation.py
    
        A class structure to store information about wordnet synsets from the index files.
        
        >>> Only storage 
        
    Translator.py
    
        A class structure to store information about ontoNotes's annotation of senses.
        
        >>> Only storage
        
        
Structure and Usage of the single program parts - Algorithm

    Onti.py
    
        This is the master class used to activate all other classes. For demonstration purposes, no customization is available at the moment.
        
        startOnti() -> Start the program
        Example:
            startOnti()
        >>> Use this funtion to get a "quick" demonstration of our project.

    WordNetSearcher.py
    
        A class that reads the data and index files of WordNet and constructs subgraphs for each input sentence.
	Step 1:
	readIndexFiles() & readDataFiles() -> read WordNet index files (*.index) and read WordNet data files and create dictionaries for each word and its synsets.
	
	Step 2:
	createTrees() -> creates all subtrees from the senses of all input words.
	createTree() -> creates a subtree for each sense of the input words. Each sense is the root of the subtree. This method applies a breadth first search with a depth of 3.
	
	Step 3:
	constructGraph() -> from the created subtrees, we construct a graph for applying the graph connectivity measures (see class Graph). For each pair of synsets that doesn't belong to the same word, we search for a path with a maximal length of 6. If we find such a path, we add this path to the final graph.

    
    
    Evaluator.py
    
        A class that coordinates the whole process and calculates the results.
	evaluate() -> evaluates the results of any given graph measure comparing with the senses annotated in OntoNotes.
    
    OntoNodesSentenceExtractor.py
    
        A class that works intersection between Evaluator.py and Data.py by providing single sentences to work on.
    
    Graph.py
    
        A class that calculates all graph measures.a
    
    Node.py
    
        A class that represents words in the sentence.
    
    Word.py
    
        	A class that represents a Word object containing the string of a word and all of its direct synsets. This object is used in the WordNetSearcher.

    
    Tree.py
   
       A class that represents a subtree that is constructed in the WordNetSearcher. It takes care of storing the information of all paths its root.

   
Structure and Usage of the single program parts - Random other stuff

    TabsToWhiteSpaces.py
    
        A function to change all occurences of tabs to 4 whitespaces in a code file and vice versa.
        Example:
            tabsToWhitespaces(file)
        >>> Not part of the actual program
   
    
        
    
