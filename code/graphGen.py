#! /usr/bin/python

from scipy.sparse import csr_matrix
import networkx as nx
import sys

class GoodreadsGraph:
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

    def _loadFromRaw(self, datafile):
        U = set()
        B = set()
        with open(datafile, "r") as f:
            for line in f:
                u, b, r = line.split(";")
                if b <> "0000000000":
                    self.g.add_node("u" + u, bipartite = 0, Type = "user")
                    self.g.add_node("b" + b, bipartite = 1, Type = "book")
                    self.g.add_edge("u" + u, "b" + b, weight = float(r))
                    U.add("u" + u)
                    B.add("b" + b)
        self.User, self.Books = list(U), list(B)


    def _loadFromGDF(self, datafile):
        U = set()
        B = set()
        with open(datafile, "r") as f:
            line = f.readline()
            if line.startswith("nodedef"):
                for line in datafile:
                    try: u, s_Type = line.split(",")
                    except ValueError: break

                    if s_type == "user":
                        self.g.add_node("u" + u, bipartite = 0, Type = s_Type)
                        U.add("u" + u)
                    elif s_type == "book":
                        self.g.add_node("b" + u, bipartite = 1, Type = s_Type)
                        B.add("b" + u)

                for line in datafile:
                    u, v, w = line.split(",")
                    self.g.add_edge("u" + u, "b" + v, weight = float(w))
            else:
                raise TypeError
        self.User, self.Books = list(U), list(B)

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
        R = []
        C = []
        D = []
        for u, v in self.g.edges_iter():
            if u.startswith('b'):
                R.append(self.Users.index(v))
                C.append(self.Books.index(u))
            else:
                R.append(self.Users.index(u))
                C.append(self.Books.index(v))
            D.append(self.g.edge[u][v]['weight'])

        a = csr_matrix((D, (R, C)), shape = (len(self.Users), len(self.Books)))
        users_mat =  a.dot(a.transpose())

        g = nx.Graph()
        r, c = users_mat.nonzero()
        g.add_weighted_edges_from(zip(r, c, users_mat.data))

        return g

if __name__ == "__main__":
    g = GoodreadsGraph(sys.argv[1], "raw")
    g.nodes()[0]
    #g.dumpGDF()

    # user_graph = g.projectUsers()

    # with open("users.gdf", "w") as f:
    #   f.write("nodedef>name VARCHAR\n")
    #   for i in user_graph.nodes_iter():
    #       f.write("{}\n".format(g.Users[i]))
    #   f.write("edgedef>node1 VARCHAR, node2 VARCHAR, weight DOUBLE\n")
    #   for i, j in user_graph.edges_iter():
    #       f.write("{},{},{}\n".format(g.Users[i], g.Users[j], user_graph[i][j]['weight']))
