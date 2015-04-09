from igraph import Graph
import louvain
import sys

def generate_bipartite(fname):
    g = Graph.Read_Ncol(fname,weights = True)
    g.vs['type'] = map(lambda x:x.startswith('u'), g.vs['name'])
    return g.bipartite_projection(which=True)
    

if __name__ == "__main__":
    one = generate_bipartite(sys.argv[1])
    #part = louvain.find_partition(one, method = 'Modularity')
