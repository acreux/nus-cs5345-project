from random import sample
import multiprocessing
from functools import partial

def clean0(reviews="user_book_raw.csv"):
    output_filename = "user_book_cleaned_0.csv"
    with open(reviews) as f,\
         open(output_filename, "w") as reviews_out:
        
        for i, line in enumerate(f):
            rating = line.rstrip().split(";")[2]
            if int(rating) > 0:
                reviews_out.write(line)
    return output_filename


def sample_reviews(size=10**4, suffix=None, reviews="user_book_raw.csv"):
    """Sample reviews"""
    
    suffix = suffix or str(size)

    user_filename = sample_users(size, suffix)
    
    print "Users saved. Start reviews filtering."

    with open(user_filename) as u:
        user_set = set(line.rstrip() for line in u)

    print len(user_set)

    output_filename = "user_book_sample_" + suffix + ".csv"
    with open(reviews) as f,\
         open(output_filename, "w") as reviews_out:
        
        for i, line in enumerate(f):
            if not i%10**6:
                print i
            user_id = line.rstrip().split(";")[0]
            if user_id in user_set:
                reviews_out.write(line)
    return output_filename

def sample_users(size=10**4, suffix=None, users="users.csv"):
    """Sample users. 
    Deprecated: Use sample_reviews instead"""

    suffix = suffix or str(size)
    with open(users) as f:
        user_set = set(line.rstrip() for line in f)
        user_sample = sample(user_set, size)

    out_filename = "user_sample_" + suffix + ".csv"
    with open("user_sample_" + suffix + ".csv", "w") as out:
        out.writelines((i + "\n" for i in iter(user_sample)))
    return out_filename

def sample_friends(users="users_sample_5.csv", friends="friends.csv"):
    """Only keep friends connections from users who are in the reviews.
    Deprecated, do not use it."""
    with open(users) as u:
        user_set = set(line.rstrip() for line in u)

    with open(friends) as f,\
         open(users.split(".")[0] + "_friends" + ".csv", "w") as out:
        
        for i, line in enumerate(f):
            if not i%10**6:
                print i
            u1, u2 = line.rstrip().split(";")
            if u1 in user_set and u2 in user_set:
                out.write(line)


if __name__ == "__main__":
    sample_friends()
