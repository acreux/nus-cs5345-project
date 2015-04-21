#! /usr/bin/python

import sys
import shelve

def reIndex(oldFile, newFile):
	user = shelve.open("usershelf")
	book = shelve.open("bookshelf")

	with open(oldFile, "r") as f:
		g = open(newFile, "w")
		i = 0
		for line in f:
			u, v, w = line.strip().split()
			g.write("%d %d %s\n" % (user[u], book[v], w))
			if i % 100000 == 0:
				print i
			i += 1
		g.close()

	user.close()
	book.close()

if __name__ == "__main__":
	reIndex(sys.argv[1], sys.argv[2])
