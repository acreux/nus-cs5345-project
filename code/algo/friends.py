from collections import defaultdict
import cPickle as pickle


class Friendship(object):

    def __init__(self, friends_csv="friends.csv", user_filename="users.csv"):
        with open(user_filename, "r") as f:
            self._set_user_index(f)
        with open(friends_csv, "r") as f:
            self._generate_friends(f)

    @staticmethod
    def load(filename="friends_pickle"):
        """Load a friends picke file"""
        with open(filename, "rb") as f:
            return pickle.load(f)
    
    def _set_user_index(self, f):
        self.user_set = set(e.rstrip() for e in f)
        self.user_index = {e:i for i, e in enumerate(list(self.user_set))}

    def _generate_friends(self, f):

        self.friends = defaultdict(set)
        f.seek(0)
        for line in f:
            u1, u2 = line.rstrip().split(";")
            if (u1 in self.user_index) & (u2 in self.user_index):
                self.friends[self.user_index[u1]].add(self.user_index[u2])

    def save(self, filename="friends_pickle"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)