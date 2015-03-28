#! /usr/bin/python

import networkx as nx
import sys

class Bipartite:
	def __init__(self, datafile = None, filetype = None):
		self.g = nx.Graph()
		self.Books = 0
		self.Users = 0

		if datafile:
			if filetype == "raw":
				self._loadFromRaw(datafile)
			elif filetype == "gdf":
				self._loadFromGDF(datafile)
			else:
				raise TypeError

		print nx.is_bipartite(self.g)
		self.Users, self.Books = nx.bipartite.sets(self.g)

	def _loadFromRaw(self, datafile):
		with open(datafile, "r") as f:
			for line in f:
				u, b, r = line.split(";")
				if b <> "0000000000":
					self.g.add_node("u" + u, bipartite = 0, Type = "user")
					self.g.add_node("b" + b, bipartite = 1, Type = "book")
					self.g.add_edge("u" + u, "b" + b, weight = float(r))


	def _loadFromGDF(self, datafile):
		with open(datafile, "r") as f:
			line = f.readline()
			if line.startswith("nodedef"):
				for line in datafile:
					try: u, s_Type = line.split(",")
					except ValueError: break

					if s_type == "user":
						self.g.add_node("u" + u, bipartite = 0, Type = s_Type)
					elif s_type == "book":
						self.g.add_node("b" + u, bipartite = 1, Type = s_Type)

				for line in datafile:
					u, v, w = line.split(",")
					self.g.add_edge("u" + u, "b" + v, weight = float(w))
			else:
				raise TypeError

	def dumpGDF(self, datafile):
		'''
			Dumps the graph 'g' in the Gephi GDF Format
		'''
		with open(datafile, "w") as f:
			f.write("nodedef>name VARCHAR,type VARCHAR\n")
			for i in self.g.nodes_iter():
				f.write("%d\t%s\n" % (i, self.g.node[i]['Type']))
			f.write("edgedef>node1 VARCHAR, node2 VARCHAR, weight DOUBLE\n")
			for i, j in self.g.edges_iter():
				f.write("%d,%d,%f\n" % (i, j, self.g.edge[i][j]['weight']))

	def loadGraph(self, graph):
		self.g = graph

	def projectUsers(self):
		'''
			Doesn't use the weight as expected
			Has to be changed
		'''
		return nx.bipartite.weighted_projected_graph(self.g, self.Users)

if __name__ == "__main__":
	g = Bipartite(sys.argv[1], "raw")
	#g.dumpGDF()

	new = g.projectUsers()

	#with open("users.gdf", "w") as f:
	#	f.write("nodedef>name VARCHAR,type VARCHAR\n")
	#	for i in new.nodes_iter():
	#		f.write("%d\n" % (i))
	#	f.write("edgedef>node1 VARCHAR, node2 VARCHAR, weight DOUBLE\n")
	#	for i, j in new.edges_iter():
	#		f.write("%d,%d\n" % (i, j))
