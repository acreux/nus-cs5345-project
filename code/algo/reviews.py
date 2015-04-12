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

    def user_to_user(self, reviews_filename="user_book_reviews.csv", suffix=None):
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

        print "users_books done"
        print size_U_T_B
        print all_combinations


        # def score_gen():
        #     i = 0
        #     for u, v in combinations(U_T_B.keys(), 2):
        #         i += 1
        #         if not i % 10**7:
        #             print i/10**7, "/",  all_combinations/10**7
        #         yield u, v, score(U_T_B_books[u], U_T_B_books[v])


            # return list(lines_gen())
            # with open(file_out, "w") as f:
            #     f.writelines(lines_gen())
        
        # 3. Generate all possible combinations between users.
        # iterable = ((u, U_T_B_books[u], v, U_T_B_books[v]) for u, v in combinations(U_T_B.keys(), 2))
        def it():
            for i, (u, v) in enumerate(combinations(U_T_B.keys(), 2)):
                if not i%10**6:
                    print i
                yield (u, U_T_B[u], U_T_B_books[u], v, U_T_B[v], U_T_B_books[v]) 

        # Multiprocessing
        pool = multiprocessing.Pool(10)
        score_func = get_score("common")
        a = pool.imap_unordered(score_func, it(), 100)

        # print len(work_multi.do(i foriterables, 10**4)))

        # def out():
        #     # Retrieve the 1000000 edges with the highest score
        #     return heapq.nlargest(10**6, score_gen(), key=itemgetter(2))
        suffix = suffix or reviews_filename.split(".")[0].split("_")[-1]
        with open("edges_" + suffix + ".csv", "w") as f:
            f.writelines(i for i in a if i)

if __name__ == "__main__":
    r = Reviews()
    r.user_to_user("user_book_sample_50.csv")