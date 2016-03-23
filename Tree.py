import Node
import Word
import sys

class Tree(object):
    def __init__(self, nodes):
        if type(nodes) == list:
            self.nodes = nodes
            self.nodes[0].sub_tree = self
        elif type(nodes) == set:
            self.nodes = list(nodes)
        else:
            sys.stderr.write('illegal type for nodes. Has to be list')
        