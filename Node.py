class Node(object):
    def __init__(self, name):
        #basic attributes
        self.name = name
        self.neighbours = []        
        
        #measures
        self.in_degree = len(self.neighbours)
        self.page_rank = 0
        self.kpp = 0
        self.betweenness = 0
        
        #stuff needed for algorithms
        self.previous_pr = 0
        self.tree_dictionary = {self: [[], 0]} #neccessary for several tree methods. has the form {Node0: [[Node1, Node2,...], distance_to_Node0]]}
        #Node0: root node of the tree; Node1, Node2: nodes wich belong to shortest paths to root node
        self.betweenness_relevance=1        
                
        
    
    
    
    