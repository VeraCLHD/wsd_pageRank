import Node

class Graph(object):
    def __init__(self, words, nodes, d):
        self.words = words
        self.nodes = nodes
        self.d = d
   
                    
    def calculatePageRank(self, d):   
        for node in self.nodes:
            node.previous_weight = 1.0/len(self.nodes) #initialize equal start weights which sum up to 1
        min_change_val = 0.01
        min_change = True #chechs after each iteration if a minimum change happend in the algorithm
        div = 1.0/len(self.nodes)
        while min_change == True: #from here the iterations begin
            min_change = False
            for node in self.nodes: #begin to fill node weights with damping partition
                node.weight = (1-d)*div
            for node in self.nodes:
                cnt_neighbours = len(node.neighbours)
                for neighbour in node.neighbours: #let weight flow from each node to its neighbours
                    neighbour.weight += d*node.previous_weight/cnt_neighbours
            for node in self.nodes: #check min_difference to previous iteration
                if abs(node.previous_weight-node.weight)>min_change_val:
                    min_change = True
                    break
            for node in self.nodes: #declare weights as old weights
                node.previous_weight = node.weight
            
                
                
if __name__ == "__main__":
    Node1 = Node.Node("00000001")    
    Node2 = Node.Node("00000002")
    Node3 = Node.Node("00000003")
    Node4 = Node.Node("00000004")
    Node5 = Node.Node("00000005")
    Node1.neighbours = [Node2, Node3, Node4, Node5]
    Node2.neighbours = [Node1, Node3]
    Node3.neighbours = [Node1, Node2]
    Node4.neighbours = [Node1]
    Node5.neighbours = [Node1]
    
    g = Graph(["Fisch"], [Node1, Node2, Node3, Node4, Node5], 0.8)
    g.calculatePageRank(g.d)
    for node in g.nodes:
        print node.weight