#! /usr/bin/python

import networkx as nx

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

		self.Users, self.Books = nx.bipartite.sets(self.g)

	def _loadFromRaw(self, datafile):
		with open(datafile, "r") as f:
			for line in datafile:
				u, b, r = line.split(";")
				if b <> "0000000000":
					g.add_node(int(u), bipartite = 0, Type = "user")
					g.add_node(int(b), bipartite = 1, Type = "book")
					g.add_edge(int(u), int(b), weight = float(r))


	def _loadFromGDF(self, datafile):
		with open(datafile, "r") as f:
			line = f.readline()
			if line.startswith("nodedef"):
				for line in datafile:
					try: u, s_Type = line.split(",")
					except ValueError: break

					if s_type == "user":
						g.add_node(int(u), bipartite = 0, Type = s_Type)
					elif s_type == "book":
						g.add_node(int(u), bipartite = 1, Type = s_Type)

				for line in datafile:
					u, v, w = line.split(",")
					g.add_edge(int(u), int(v), weight = float(w))
			else:
				raise Error

	def dumpGDF(self, datafile):
		'''
			Dumps the graph 'g' in the Gephi GDF Format
		'''
		with open(datafile, "w") as f:
			f.write("nodedef>name VARCHAR,type VARCHAR\n")
			for i in self.g.nodes_iter():
				f.write("%d\t%s\n" % (i, g.node[i]['Type']))
			f.write("edgedef>node1 VARCHAR, node2 VARCHAR, weight DOUBLE\n")
			for i, j in self.g.edges_iter():
				f.write("%d,%d,%f\n" % (i, j, g.edge[i][j]['weight']))

	def projectUsers(self):
		'''
			Doesn't use the weight as expected
			Has to be changed
		'''
		return nx.bipartite.weighted_projected_graph(g, self.Users)
