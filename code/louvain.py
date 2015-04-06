import community
import networkx as nx
import sys

def read_graph(fname):
	g = nx.Graph()
	with open(fname, "r") as f:
		edges = map(lambda x: (x[0], x[1], float(x[2])), (line.strip().split(',') for line in f))
	g.add_edges_from(edges)

	return g

if __name__ == "__main__":
	G = read_graph(sys.argv[1])

	dendro = community.generate_dendrogram(G)

	for i in range(len(dendro)):
		print "Partition at level:"
		# Returns dictionary
		print community.partition_at_level(dendro, i)
		print "Modularity:", community.modularity(dendro[i])

	
