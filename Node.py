import sys
class Node(object):
    nodes = []
    counter = 0
    def __init__(self, name):
        self.counter = Node.counter+0
        Node.counter +=1
        #basic attributes
        found = False
        #if type(name) == str:
        self.name = name
        #else:
            #sys.stderr.write('illegal type for name. Has to be str')
        Node.nodes.append(self)
        self.neighbours = set()
        self.sub_tree = None
        #measures
        self.in_degree = 0
        self.page_rank = 0
        self.personalized_page_rank = 0
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
        
    def __hash__(self):
        return hash(self.name)
        
    def __repr__(self):
        return str(self.counter)
    
    @staticmethod
    def createNode(name):
        for node in Node.nodes:
            if node.__hash__() == hash(name):
                return node
        return Node(name)
        
    def initializeInDegree(self):
        self.in_degree = len(self.neighbours)
        
    def initializeResidualGraph(self): #must be done after the graph is created
        for neighbour in self.neighbours:
            self.residual_graph_neighbours[neighbour] = 0 #0 means no flow yet. 1 and -1 mean flow on some direction
        
    
    def resetResidualValues(self):
        for key in self.residual_graph_neighbours.keys():
            self.residual_graph_neighbours[key] = 0

if __name__ == "__main__":
    node1 = Node.createNode("a")
    node2 = Node.createNode("a")
    print node1 == node2
    
    