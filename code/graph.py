#! /usr/bin/python

from scipy.sparse import csr_matrix
import networkx as nx
import sys
from networkx.algorithms import bipartite
import cPickle as pickle


class GoodreadsGraph(nx.Graph):

    def __init__(self, datafile=None, filetype=None):
        nx.Graph.__init__(self)
        self._books = None
        self._users = None
        self._projected_users = None
        if datafile:
            self.datafile = datafile

        if datafile:
            if filetype == "raw":
                self._loadFromRaw(datafile)
            elif filetype == "gdf":
                self._loadFromGDF(datafile)
            else:
                raise TypeError

        self.graph_name = self.datafile + "_graph"
        self.adjacency_matrix_name = self.datafile + "_adjacency_csr"
        self.users_matrix_name = self.datafile + "_user_csr"
        self.users_graph_name = self.datafile + "_user_graph"

    def _loadFromRaw(self, datafile):
        with open(datafile, "r") as f:
            # Add edges
            self.add_weighted_edges_from(((("u"+line.split(";")[0]),
                                           ("b"+line.split(";")[1]),
                                           float(line.split(";")[2])) for line in f))
            # for line in f:
            #     u, b, r = line.split(";")
            #     self.add_node("u" + u, bipartite=0, type="user")
            #     self.add_node("b" + b, bipartite=1, type="book")
            #     self.add_edge("u" + u, "b" + b, weight = float(r))

    @property
    def users(self):
        if not self._users:
            self._users = set((n for n in self.nodes() if n[0]=="u"))
        return self._users

    @property
    def books(self):
        if not self._books:
            self._books = set((n for n in self.nodes() if n[0]=="b"))
        return self._books

    def save(self, filename=None):
        """Save a graph using pickle"""
        file_name = filename or self.datafile+"_graph"
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        """Load a graph picke file"""
        with open(filename, "rb") as f:
            return pickle.load(f)

    # @property
    # def projected_users(self):
    #     if not self._projected_users:
    #         self._projected_users = bipartite.projected_graph(g, g.users)
    #     return self._projected_users

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

    def compute_adjacency_matrix(self):
        user_list = list(self.users)
        book_list = list(self.books)

        csr_generator = [(user_list.index(node), book_list.index(neighbor), val['weight'])\
                            for node, node_dict in self.adjacency_iter()\
                            for neighbor, val in node_dict.iteritems() if node.startswith("u")]
        rows, columns, data = zip(*csr_generator)
        a = csr_matrix((data, (rows, columns)), shape=(len(user_list), len(book_list)))
        with open(self.adjacency_matrix_name, "wb") as f:
            pickle.dump(a, f)  

    def adjacency_csr(self):
        return GoodreadsGraph.load(self.adjacency_matrix_name)

    def compute_users_matrix(self):
        csr_mat = self.adjacency_csr()
        users_mat = csr_mat.dot(csr_mat.transpose())
        with open(self.users_matrix_name, "wb") as f:
            pickle.dump(users_mat, f)

    def users_matrix(self):
        return GoodreadsGraph.load(self.users_matrix_name)

    def compute_users_graph(self):
        g = nx.Graph()
        users_mat = self.users_matrix()
        r, c = users_mat.nonzero()
        g.add_weighted_edges_from(zip(r, c, users_mat.data))

        with open(self.users_graph_name, "wb") as f:
            pickle.dump(g, f)

    def users_graph(self):
        return pickle.load(self.users_graph_name)

    def generate_projected_users(self):
        self.compute_adjacency_matrix()
        self.compute_users_matrix()
        self.compute_users_graph()


if __name__ == "__main__":
    g = GoodreadsGraph("data/small", "raw")
    g.generate_projected_users()
    # g.save("graph_all")
    # g = GoodreadsGraph.load("graph_all")
    print len(list(g.users))
    # GoodreadsGraph.load("graph0")
    # G = bipartite.projected_graph(g, g.users)
    # biadjacency_matrix(g, list(g.users()), list(g.))
    # with open("graph_user", "w") as f:
    #     pickle.dump(e, f)
