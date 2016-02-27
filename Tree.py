import Node
import Word

class Tree(object):
	def __init__(self, nodes):
		if type(nodes) == list:
			self.nodes = nodes
			self.nodes[0].sub_tree = self
		else:
			sys.stderr.write('illegal type for nodes. Has to be list')
		