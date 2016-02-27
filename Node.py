import sys
class Node(object):
    def __init__(self, name):
        #basic attributes
        if type(name) == str:
            self.name = name
        else:
            sys.stderr.write('illegal type for name. Has to be str')
        self.neighbours = []        
        self.sub_tree = None
        #measures
        self.in_degree = 0
        self.page_rank = 0
        self.kpp = 0
        self.betweenness = 0
        self.residual_value = 0
        
        #stuff needed for algorithms
        self.previous_pr = 0
        self.tree_dictionary = {self: [[], 0]} #neccessary for several tree methods. has the form {Node0: [[Node1, Node2,...], distance_to_Node0]]}
        #Node0: root node of the tree; Node1, Node2: nodes wich belong to shortest paths to root node
        self.betweenness_relevance=1
        self.residual_graph_neighbours = {}
        self.predecessor = None #needed for bfs for maximum flow
        
        
    def initializeInDegree(self):
        self.in_degree = len(self.neighbours)
        
    def initializeResidualGraph(self): #must be done after the graph is created
        for neighbour in self.neighbours:
            self.residual_graph_neighbours[neighbour] = 0 #0 means no flow yet. 1 and -1 mean flow on some direction
        
    
    def resetResidualValues(self):
        for key in self.residual_graph_neighbours.keys():
            self.residual_graph_neighbours[key] = 0
    
    def getNeighbours(self):
	    return self.neighbours
    def setNeighbours(self, neighbours):
		self.neighbours = neighbours
    def getName(self):
	    return self.name
    def setName(self, name):
	    self.name = name
    
    
    
    