import Node
import Word

class Tree(object):
	def __init__(self, nodes):
		if type(nodes) == list:
			self.nodes = nodes
		else:
			sys.stderr.write('illegal type for nodes. Has to be list')
		
		self.tree_dictionary = {self: [[], 0]} #has the form {Node0: [[Node1, Node2,...], distance_to_Node0]]}
		