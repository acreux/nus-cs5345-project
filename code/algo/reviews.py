from collections import defaultdict
import cPickle as pickle
import fileinput
from itertools import combinations
import heapq
from operator import itemgetter



class Reviews(object):
    """Class handling reviews"""

    def __init__(self):
        self._book_to_user = None
        self._user_to_book = None
        
    @staticmethod
    def load(filename="reviews_pickle"):
        """Load a reviews picke file"""
        with open(filename, "rb") as f:
            return pickle.load(f)

    def load_csv(self, filename="reviews.csv"):
        self._generate_user_to_book(f)

    def save(self, filename="reviews_pickle"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def save_user_to_book(self, filename="user_to_book_pickle"):
        with open(filename, "wb") as f:
            pickle.dump(self.user_to_book, f)

    def _generate_user_to_book(self, filename="test1.csv"):
        user_to_book = defaultdict(set)
        with open(filename, "r") as f:
            for line in f:
                book, user, rating = line.rstrip().split(";")
                user_to_book[user].add((book, rating))
        return user_to_book

    @property
    def user_to_book(self):
        if not self._user_to_book:
            self._user_to_book = self._generate_user_to_book()
        return self._user_to_book

    def save_book_to_user(self, filename="book_to_user_pickle"):
        with open(filename, "wb") as f:
            pickle.dump(self.book_to_user, f)

    def clean_reviews(self, filename="reviews.csv"):
        book_cpt, last_book_id = 0, ""
        user_cpt, last_user_id = 0, ""

        f = fileinput.FileInput(filename, inplace=True)
        for line in f:
            new_book_id, new_user_id, rating = line.rstrip().split(";")
            if new_book_id != last_book_id:
                book_cpt += 1
                last_book_id = new_book_id

            if new_user_id != last_user_id:
                user_cpt += 1
                last_user_id = new_user_id

            print ";".join([str(book_cpt), str(user_cpt), rating])
        f.close()
    
    @property
    def book_to_user(self):
        if not self._book_to_user:
            self._book_to_user = self._generate_book_to_user()
        return self._book_to_user

    def _generate_book_to_user(self, filename="test1.csv"):

        book_to_user = defaultdict(set)
        with open(filename, "r") as f:
            for line in f:
                book, user, rating = line.rstrip().split(";")
                book_to_user[book].add((user, rating))
        return book_to_user

    def user_to_user(self, reviews_filename="reviews.csv"):
        threshold = 10
        def score(l1, l2):
            a = set(zip(*l1)[0])
            if len(a) < threshold:
                return 0
            return len(a.intersection(zip(*l2)[0]))

        U_T_B = self.user_to_book

        print "users_books done"
        i = 0
        for u, v in combinations(U_T_B.keys(), 2):
            i += 1
            if not i % 10000000:
                print i
            if score(U_T_B[u], U_T_B[v]) >= threshold:
                yield (u, v) 

    def user_to_user_too_long(self, reviews_filename="reviews.csv"):

        def basic_score(rating1, rating2):
            """Score between two users. Only based on the ratings"""
            return rating1 + rating2

        def mix(user_rating_set):
            for i, j in combinations(user_rating_set, 2):
                u1, r1 = i
                u2, r2 = j
                yield u1, r1, u2, r2, basic_score(int(r1), int(r2))

        def score_gen():
            with open(reviews_filename) as f:

                last_book_id = ""
                book_bucket = set()

                i = 0
                for line in f:
                    i += 1
                    if not i % 10**1:
                        print i
                    book, user, rating = line.rstrip().split(";")

                    if book == last_book_id:
                        book_bucket.add((user, rating))
                    else:
                        print last_book_id, " start"
                        for edge in mix(book_bucket): yield edge
                        print last_book_id, " end"
                        last_book_id = book
                else:
                    for edge in mix(book_bucket): yield edge

        return heapq.nlargest(1000, score_gen(), key=itemgetter(4))

if __name__ == "__main__":
    r = Reviews()
    r.user_to_user()

    i = 0
    for _ in r.user_to_user():
        if not i %  10**3:
            print i