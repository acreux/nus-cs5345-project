# import igraph
from collections import defaultdict
from igraph import Graph, summary
import igraph
import louvain
from time import time
import numpy as np
import csv
import io


class UserGraph(Graph):

    def __init__(self, edges_filename):
        self.edges_filename = edges_filename
        edges_gen = self._load_edges(edges_filename)
        Graph.__init__(self, list(edges_gen))

        self._friends = None
        self._partitions = None
        self._homophily = None

        self.score_f = self.edges_filename.split(".")[0].split("_")[1]
        self.sample_id = self.edges_filename.split(".")[0]

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
        self._partitions = {}
        self.partitions_timer = {}
        
        now = time()
        self._partitions["louvain"] = Partition(louvain.find_partition(self, method="Modularity"))
        self.partitions_timer["louvain"] = int(time()-now)
        print "louvain"
        
        now = time()
        self.partitions["community_fastgreedy"] = Partition(self.community_fastgreedy().as_clustering())
        self.partitions_timer["community_fastgreedy"] = int(time()-now)
        print "community_fastgreedy"

        now = time()
        self.partitions["community_infomap"] = Partition(self.community_infomap())
        self.partitions_timer["community_infomap"] = int(time()-now)
        print "community_infomap"

        now = time()
        self.partitions["community_leading_eigenvector"] = Partition(self.community_leading_eigenvector())
        self.partitions_timer["community_leading_eigenvector"] = int(time()-now)
        print "community_leading_eigenvector"

        now = time()
        self.partitions["community_label_propagation"] = Partition(self.community_label_propagation())
        self.partitions_timer["community_label_propagation"] = int(time()-now)
        print "community_label_propagation"

        now = time()
        self.partitions["community_multilevel"] = Partition(self.community_multilevel())
        self.partitions_timer["community_multilevel"] = int(time()-now)
        print "community_multilevel"

        # now = time()
        # self.partitions["community_optimal_modularity"] = Partition(self.community_optimal_modularity())
        # self.partitions_timer["community_optimal_modularity"] = int(time()-now)
        # print "community_optimal_modularity"

        # now = time()
        # self.partitions["community_edge_betweenness"] = Partition(self.community_edge_betweenness().as_clustering())
        # self.partitions_timer["community_edge_betweenness"] = int(time()-now)
        # print "community_edge_betweenness"

        now = time()
        self.partitions["community_spinglass"] = Partition(self.community_spinglass())
        self.partitions_timer["community_spinglass"] = int(time()-now)
        print "community_spinglass"

        now = time()
        self.partitions["community_walktrap"] = Partition(self.community_walktrap().as_clustering())
        self.partitions_timer["community_walktrap"] = int(time()-now)
        print "community_walktrap"

    @property
    def friends(self):
        if not self._friends:
            self._friends = self._compute_friends_index()
        return self._friends

    @property
    def friends_size(self):
        """How many friends relationships?"""
        return sum(len(i) for i in self.friends.values())/2

    @property
    def friends_alone(self):
        """How many readers are alone?"""
        return sum(1 for v in self.friends.values() if len(v)==0)

    @property
    def friends_median(self):
        """How many readers are alone?"""
        return np.median([len(i) for i in self.friends.values()])

    @property
    def partitions(self):
        """Dict for each parition, the cluster"""
        if not self._partitions:
            self._generate_partition()
        return self._partitions

    def _compute_friends_index(self, friends_filename="friends.csv"):
        """Retrieve friends using the index created"""
        friends_index = defaultdict(set)
        users = set(self.user_index.keys())
        with open(friends_filename) as f:
            for i, line in enumerate(f):
                # if not i%10**6:
                #     print i
                u1, u2 = line.rstrip().split(";")
                if (u1 in users) and (u2 in users):
                    friends_index[self.user_index[u1]].add(self.user_index[u2])
                    friends_index[self.user_index[u2]].add(self.user_index[u1])
        return friends_index

    @property
    def homophily(self):
        """Dict for each parition, the homophily score"""
        if not self._homophily:
            self._homophily = self._generate_homophily()
        return self._homophily

    def _generate_homophily(self):
        return {name: partition.homophily(self.friends) for name, partition in self.partitions.iteritems()}

    def results_gen(self):
        results = {"sample_id": self.sample_id,
                   "score": self.score_f,
                   "size_user": str(len(self.vs)),
                   "size_edges": str(len(self.es)),
                   "size_friends": str(self.friends_size),
                   "friends_median": str(self.friends_median),
                   "friends_alone": str(self.friends_alone)}
        for algo in  ["louvain", "community_fastgreedy", "community_infomap",\
                      "community_leading_eigenvector",\
                      "community_label_propagation", "community_multilevel",\
                      "community_edge_betweenness",\
                      "community_spinglass", "community_walktrap"]:
            new_dict = dict(results)
            try:
                pass
            except Exception as e:
                print algo
                print e
            else:
                clusters_keys = self.partitions[algo].clusters.keys()
                new_dict.update({
                    "detection_algo": algo,
                    "detection_algo_time": self.partitions_timer[algo],
                    "global_homophily": "{:.3f}".format(self.homophily[algo]),
                    "clusters_size": ",".join([str(self.partitions[algo].clusters_size[k]) for k in clusters_keys]),
                    "clusters_homophily": ",".join(["{:.3f}".format(self.partitions[algo].homophily_dict[k]) for k in clusters_keys]),
                    "clusters_modularity": ",".join(["{:.3f}".format(self.partitions[algo].modularity) for k in clusters_keys])})
                yield new_dict


    def write_results(self):
        output_filename = "results.csv"
        fieldnames = ["sample_id", "score", "size_user","size_edges", "size_friends", "friends_alone", "friends_median", "detection_algo", "detection_algo_time",
                      "global_homophily", "clusters_size", "clusters_homophily", "clusters_modularity"]

        rows_gen = self.results_gen()
        with io.open(output_filename, "ab") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            # w.writeheader()
            for r in rows_gen:
                w.writerow(r)


class Partition(igraph.clustering.VertexClustering):

    def __init__(self, vc):
        self.vc = vc
        self.clusters = dict(enumerate(vc))
        self.clusters_size = {k:len(v) for k, v in self.clusters.iteritems()}
        self.homophily_dict = None

    @property
    def modularity(self):
        return self.vc.modularity

    def homophily(self, friends_index):
        """Return list of parition homophily and size of each partition"""
        if not self.homophily_dict:
            self.homophily_dict = {k: self._get_cluster_homophily(v, friends_index) for k, v in self.clusters.iteritems()}
        return np.mean(self.homophily_dict.values())

    def _get_cluster_homophily(self, clst, friends_index):
        """
        Homophily:
        How many friends are in the book community?
        # This calculates homophily for largest community"""
        h = 0
        for member in clst:

            num = len(friends_index[member].intersection(clst))
            den = len(friends_index[member])
            if den == 0:
                if num != 0:
                    raise Exception("Error: Not Possible")
            else:
                h += 1. * num / den
            
        return 1. * h / len(clst)


if __name__ == "__main__":
    g = UserGraph("edges_common_50.csv")
    g.write_results()

