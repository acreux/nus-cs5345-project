from collections import defaultdict
import cPickle as pickle

class Reviews(object):

    def __init__(self, reviews_csv="reviews.csv"):
        with open(reviews_csv, "r") as f:
            self._generate_user_to_book(f)

    @staticmethod
    def load(filename="reviews_py"):
        """Load a reviews picke file"""
        with open(filename, "rb") as f:
            return pickle.load(f)
    
    def _generate_user_to_book(self, f):

        f.seek(0)
        books_set = set((e.rstrip().split(";")[1] for i, e in enumerate(f)))
        book_index = {e:i for i, e in enumerate(list(books_set))}

        f.seek(0)
        users_set = set((e.rstrip().split(";")[0] for i, e in enumerate(f)))
        user_index = {e:i for i, e in enumerate(list(users_set))}

        f.seek(0)
        self.user_to_book = defaultdict(set)
        for line in f:
            user, book, rating = line.rstrip().split(";")
            self.user_to_book[user_index[user]].add(book_index[book])
    
    def book_to_user(self):
        book_to_user = defaultdict(set)

        for user, book_list in self.user_to_book.iteritems():
            for book in book_list:
                book_to_user[book].add(user)
        return book_to_user

    def save(self, filename="reviews_py"):
        """Save a graph using pickle"""
        with open(filename, "wb") as f:
            pickle.dump(self, f)