from collections import defaultdict
import cPickle as pickle
import fileinput
from functools import partial
from itertools import combinations, izip_longest
import heapq
from operator import itemgetter
import multiprocessing
from multip import Multiprocessing

from scores import get_score
# Reviews handle friends, user and book processing tasks
# 

class Reviews(object):
    """Class handling reviews"""

    def __init__(self):
        self._book_to_user = None
        self._user_to_book = None
        
    def user_to_book(self, filename="user_book_reviews.csv"):
        """
        Return the dict with user as a key and a set of (book_id, rating) as value
        """
        user_to_book = defaultdict(set)
        with open(filename, "r") as f:
            for line in f:
                user, book, rating = line.rstrip().split(";")
                user_to_book[user].add((book, rating))
        return user_to_book

    def book_to_user(self, filename="book_user_reviews.csv"):
        """
        Return the dict with a book_id as a key and a set of (user_id, rating) as value
        """

        book_to_user = defaultdict(set)
        with open(filename, "r") as f:
            for line in f:
                book, user, rating = line.rstrip().split(";")
                book_to_user[book].add((user, rating))
        return book_to_user

    def user_to_user(self, reviews_filename="user_book_reviews.csv", suffix=None, score="common"):
        """
        1. Get the user_book dict
        2. Create the dict { user_id: set(book_read)}
        3. Generate all possible combinations between users.
        4. Define a score functions outside the class.
        5. Iterate over all combinations and write the result in an output
        """

        U_T_B = self.user_to_book(reviews_filename)

        # Get the books only
        U_T_B_books = {k: set(zip(*v)[0]) for k, v in U_T_B.iteritems()}
        
        size_U_T_B = len(U_T_B)
        all_combinations = (size_U_T_B * (size_U_T_B-1))/2
        step = all_combinations/20
        print "users_books done"
        print "Users: ", size_U_T_B
        print "Number of combinations to compute: ", all_combinations

        # 3. Generate all possible combinations between users.
        # iterable = ((u, U_T_B_books[u], v, U_T_B_books[v]) for u, v in combinations(U_T_B.keys(), 2))
        def it():
            for i, (u, v) in enumerate(combinations(U_T_B.keys(), 2)):
                if not i%step:
                    print str(i).rjust(5), "/", all_combinations, " - ",  (i*20+1)/all_combinations, "/", 20, " - "
                yield (u, U_T_B[u], U_T_B_books[u], v, U_T_B[v], U_T_B_books[v]) 
        
        # ##################################
        # Chooose your own score function in scores.py
        # ##################################
        score_func = get_score(score)

        # Multiprocessing
        pool = multiprocessing.Pool(10)

        # chunksize=100. May pout it higher to speed it up
        a = pool.imap_unordered(score_func, it(), 100)

        suffix = suffix or reviews_filename.split(".")[0].split("_")[-1]

        with open("_".join(["edges", score, suffix]) + ".csv", "w") as f:
            for ind_line, line in enumerate(a):
                if ind_line>10**7:
                    raise Exception("Too many edges.")
                if line:
                    f.writelines(line)
        print ind_line, " edges created"

if __name__ == "__main__":
    r = Reviews()
    r.user_to_user("user_book_sample_1000.csv")
