import community
import networkx as nx
import sys

def read_graph(fname):
	g = nx.Graph()

	# Get the edges
	def edges_gen():
		with open(fname, "r") as f:
			for line in f:
				user_id, book_id, weight = line.strip().split(';') 
				yield user_id, book_id, {"weight":float(weight[2])}
	
	g.add_edges_from(edges_gen())
	return g

if __name__ == "__main__":
	G = read_graph(sys.argv[1])

	#dendro = community.generate_dendrogram(G)

	#for i in range(len(dendro)):
	#	print "Partition at level:"
	#	# Returns dictionary
	#	print community.partition_at_level(dendro, i)
	#	print "Modularity:", community.modularity(dendro[i])

	
