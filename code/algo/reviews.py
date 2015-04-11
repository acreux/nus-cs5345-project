from collections import defaultdict
import cPickle as pickle
import fileinput
from itertools import combinations
import heapq
from operator import itemgetter



class Reviews(object):

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

    def _generate_user_to_book(self, filename="reviews.csv"):
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

    def _generate_book_to_user(self, filename="reviews.csv"):

        book_to_user = defaultdict(set)
        with open(filename, "r") as f:
            for line in f:
                book, user, rating = line.rstrip().split(";")
                book_to_user[book].add((user, rating))
        return book_to_user

    def user_to_user(self, reviews_filename="reviews.csv"):

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
                    if not i % 10**5:
                        print i
                    book, user, rating = line.rstrip().split(";")

                    if book == last_book_id:
                        book_bucket.add((user, rating))
                    else:
                        for edge in mix(book_bucket): yield edge
                        last_book_id = book


                else:
                    for edge in mix(book_bucket): yield edge

        return heapq.nlargest(10, score_gen(), key=itemgetter(4))


