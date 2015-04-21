from scipy.sparse import csr_matrix
import sys
import shelve
import pickle

def buildMatrix(fname):
	d_user = shelve.open("usershelf")
	d_book = shelve.open("bookshelf")

	R = []
	C = []
	D = []
	with open(fname) as f:
		i = 0
		for line in f:
			u, v, w = line.strip().split()
			R.append(d_user[u])
			C.append(d_book[v])
			D.append(float(w))
			if i % 100000 == 0:
				print i
			i += 1

	a = csr_matrix((D, (R, C)), shape = (len(d_user), len(d_book)))
	print "User Book Matrix Created: ", a.shape
	pickle.dump(a, open("users_book_mat", "w"))
	users_mat = a.dot(a.transpose())

	pickle.dump(users_mat, open("users_mat", "w"))
	return a
			
if __name__ == "__main__":
	m = buildMatrix(sys.argv[1])
