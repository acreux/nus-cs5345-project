# import igraph
from collections import defaultdict
from igraph import Graph, summary
import louvain


# class FriendsGraph(Graph):

#     def __init__(self, edges_filename):


#     def load_edges(self, filename, index):
#     friends = defaultdict(set)
#     with open(fname, "r") as f:
#         for line in f:
#             u, v = line.strip().split(';')
#             friends[int(u)].add(int(v))
#             friends[int(v)].add(int(u))
#     return friends

class UserGraph(Graph):

    def __init__(self, edges_filename):
        edges_gen = self._load_edges(edges_filename)
        Graph.__init__(self, list(edges_gen))

        self._friends = None
        self._partition = None
        # self.add_edges(edges_gen)

    def _load_edges(self, filename):
        """Nodes index is created during the csv loading"""
        self.user_index = {}

        def edges_gen():
            """Igraph requires to add integers (1..n).
            Create the user id on the fly, as we send the edges"""
            user_cpt = 0

            with open(filename, "r") as f:
                for line in f:
                    u, v, score = line.rstrip().split(";")
                    # If u already in self.user_index, return the value
                    # If not, create it.
                    u_index = self.user_index.setdefault(u, user_cpt)
                    # new u_index, we update the user counter
                    if u_index == user_cpt:
                        user_cpt +=1
                    v_index = self.user_index.setdefault(v, user_cpt)
                    if v_index == user_cpt:
                        user_cpt +=1
                    # yield u_index, v_index, float(score)
                    yield u_index, v_index
        return edges_gen()

    def _generate_partition(self):
        #return self.community_multilevel()
        return louvain.find_partition(self, method="Modularity")
        #return self.community_label_propagation()
    @property
    def friends(self):
        if not self._friends:
            self._friends = self._generate_friends_index()
        return self._friends

    @property
    def partition(self):
        if not self._partition:
            self._partition = self._generate_partition()
        return self._partition

    def _generate_friends_index(self, friends_filename="friends.csv"):
        """Retrieve friends using the index created"""
        friends_index = defaultdict(set)
        users = set(self.user_index.keys())
        with open(friends_filename) as f:
            for i, line in enumerate(f):
                if not i%10**6:
                    print i
                u1, u2 = line.rstrip().split(";")
                if (u1 in users) and (u2 in users):
                    friends_index[self.user_index[u1]].add(self.user_index[u2])
                    friends_index[self.user_index[u2]].add(self.user_index[u1])
        return friends_index

    def homophily(self, i):
        """
        Homophily:
        How many friends are in the book community?
        # This calculates homophily for largest community"""
        h = 0
        for member in self._partition[i]:

            num = len(self.friends[member].intersection(self._partition[i]))
            den = len(self.friends[member])
            if den == 0:
                if num != 0:
                    raise Exception("Error: Not Possible")
            else:
                h += 1. * num / den
            
        return 1. * h / len(self._partition[i]), len(self._partition[i])


if __name__ == "__main__":
    g = UserGraph("random_edges_rating_5000_0_7.csv")
    print summary(g)

    print sum([len(v) for v in g.friends.itervalues()])
    p = g.partition
    print p.summary()
    
    glob_hom = 0
    for i in range(len(p)):
        hom, length =  g.homophily(i)
        glob_hom += hom
        print hom, length
    print "global homophily: " + str(float(glob_hom)/len(p))
    
