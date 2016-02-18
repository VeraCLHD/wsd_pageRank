class Node(object):
    def __init__(self, name):
        self.name = name
        self.neighbours = []
        self.previous_weight = 0
        self.weight = 0
                
        self.in_degree = len(self.neighbours)
    
    
    
    