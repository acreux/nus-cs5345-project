from collections import defaultdict
from igraph import Graph
from random import choice
import itertools as it
import louvain
import pickle
import sys
import time

user_significance = 1000	# Those users who have read at least 1000 books
threshold = 20

def counted(fn):
	def wrapper(*args, **kwargs):
		wrapper.called+= 1
		if wrapper.called % 10000 == 0:
			print wrapper.called
		return fn(*args, **kwargs)
	wrapper.called= 0
	wrapper.__name__= fn.__name__
	return wrapper

@counted
def score(u, v):
	a = set(zip(*U_T_B[u])[0])
	b = set(zip(*U_T_B[v])[0])
	# I think following condition is not required
	if len(a) < user_significance or len(b) < user_significance:
		return 0
	if len(a.intersection(b)) < threshold:
		return (u, v)
	else:
		return None
		
def user_book_index(fname):
	temp = defaultdict(list)
	with open(fname, "r") as f:
		i = 0
		for line in f:
			u, b, r = line.strip().split(';')
			temp[u].append((b, r))
			if i % 1000000 == 0:
				print i
			i += 1
			
	U_T_B = dict((k, v) for k, v in temp.iteritems() if len(v) >= user_significance)
	del temp
	return U_T_B

def user_user_edges(U_T_B):
	e = [ score(u, v) for u, v in it.combinations(U_T_B.keys(), 2) ]
	edges = []
	for i in e:
		if i: edges.append(i)
	del e
	pickle.dump(edges, open("users_%d.pkl" % len(U_T_B), "wb"))
	return edges

def build_index(edges):
	i = 0
	index = {}	# goodreads_id -> igraph_id
	rev_index = {}	# igraph_id -> goodreads_id
	for u, v in edges:
		if int(u) not in index:
			index[int(u)] = i
			rev_index[i] = int(u)
			i += 1
		if int(v) not in index:
			index[int(v)] = i
			rev_index[i] = int(v)
			i += 1
	return index, rev_index

def graphGen(edges, index):
	return Graph([ (index[int(u)], index[int(v)]) for u, v in edges ])

def getCommunities(part, rev_index):
	comm = defaultdict(set)
	for vertex, community in enumerate(part.membership):
		comm[community].add(rev_index[vertex])
	return comm

def generate_friend_index(fname):
	friends = defaultdict(set)
	with open(fname, "r") as f:
		for line in f:
			u, v = line.strip().split(';')
			friends[int(u)].add(int(v))
			friends[int(v)].add(int(u))
	return friends

def calculate_homophily(comm, friends, index):
	# This calculates homophily for largest community
	h = 0
	for member in comm[0]:
		num = len(friends[member].intersection(comm[0]))
		den = len([ i for i in friends[member] if i in index ])
		if den == 0 and num != 0:
			print "Error: Not Possible"
			sys.exit(1)
		if den == 0 and num == 0: continue
		h += (num / float(den))
	return h / len(comm[0])

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: %s <user_book_csv> <friends_csv>" % sys.argv[0]
		sys.exit(1)

	# Build user to book index
	# U_T_B = {
	#	goodread_id: [
	#		(book_id, rating),
	#		...
	#	]
	# }
	U_T_B = user_book_index(sys.argv[1]))
	print "Users: ", len(U_T_B)

	# Build user-user edges based on the score function
	# This is takes most of the time (actually hours)
	# Time depends on the score function you choose 
	edges = user_user_edges(U_T_B) 
	del U_T_B

	# index = { goodreads : igraph }
	# rev_index = { igraph : goodreads }
	index, rev_index = build_index(edges)
	g = graphGen(edges, index)
	print "Generated Graph"
	del edges

	# Comm contains goodreads index
	part = louvain.find_partition(g, method = "Modularity")
	comm = getCommunities(part, rev_index)
	print "Communities Found"

	friends = generate_friend_index("friends.csv")
	print "Friend Index Built"
	#friends = generate_friend_index(sys.argv[2])

	# Homophily
	h = calculate_homophily(comm, friends, index)
	print h
