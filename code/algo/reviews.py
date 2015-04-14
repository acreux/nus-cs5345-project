from collections import defaultdict
import cPickle as pickle
import fileinput
from functools import partial
from itertools import combinations, izip_longest
import heapq
from operator import itemgetter
import multiprocessing
from multip import Multiprocessing
import time


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

    def user_to_user(self, reviews_filename="user_book_reviews.csv", suffix=None, score="common", threshold=100, chunksize=50000, process=10):
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
        U_T_B_book_ratings = {k: {book: int(rating) for book, rating in v} for k, v in U_T_B.iteritems()}
        
        size_U_T_B = len(U_T_B)
        all_combinations = (size_U_T_B * (size_U_T_B-1))/2
        step_size = 100
        step = all_combinations/step_size
        print "users_books done"
        print "Users: ", size_U_T_B
        print "Number of combinations to compute: ", all_combinations

        # 3. Generate all possible combinations between users.
        # iterable = ((u, U_T_B_books[u], v, U_T_B_books[v]) for u, v in combinations(U_T_B.keys(), 2))
        def it():
            for i, (u, v) in enumerate(combinations(U_T_B.keys(), 2)):
                # logging
                if not i%step:
                    print str(i).rjust(5), "/", all_combinations, " - ",  (i*step_size+1)/all_combinations, "/", step_size, " - "
                yield u, U_T_B_book_ratings[u], U_T_B_books[u], v, U_T_B_book_ratings[v], U_T_B_books[v]
        
        # ##################################
        # Chooose your own score function in scores.py
        # ##################################
        score_func = get_score(score, threshold)

        # Multiprocessing
        pool = multiprocessing.Pool(process)

        # Return only correct edges
        edges_created_gen = (edge for edge in pool.imap_unordered(score_func, it(), chunksize) if edge)

        def save_edges(edges_gen):
            n0 = time.time()
            time_cpt = 0

            edges_suffix = suffix or reviews_filename.split(".")[0].split("_")[-1]
            with open("_".join(["edges", score, edges_suffix]) + ".csv", "w") as f:
                ind_line = 0
                for ind_line, line in enumerate(edges_gen):
                    if ind_line>10**7:
                        raise Exception("Too many edges.")
                    if not ind_line%10**4:
                        print ind_line, " edges created"
                    f.writelines(line)

                    now = time.time()
                    if now - n0 > 100:
                        time_cpt += int(now - n0)
                        print "time: ", time_cpt, " seconds"
                        n0 = now

                print ind_line, " edges created"

        save_edges(edges_created_gen)

if __name__ == "__main__":
    r = Reviews()
    r.user_to_user("user_book_sample_50.csv", score="same_rating_2", threshold=0, chunksize=50000, process=10)
