from random import sample

def sample_reviews(size=10**4, suffix=None, reviews="user_book_raw.csv"):
    
    suffix = suffix or str(size/100)
    with open(reviews) as f:

        user_set = set(int(line.rstrip().split(";")[0]) for line in f)
        user_sample = sample(user_set, size)

        # Save users
        with open("user_sample_" + suffix + ".csv", "w") as users_out:
            users_out.writelines((str(i) + "\n" for i in iter(user_sample)))
        
        f.seek(0)
        with open("user_book_sample_" + suffix + ".csv", "w") as reviews_out:
            for i, line in enumerate(f):
                if not i%10**6:
                    print i
                if int(line.rstrip().split(";")[0]) in user_sample:
                    reviews_out.write(line)

def sample_users(size=10**4, users="users.csv"):
    """Sample users. 
    Deprecated: Use sample_reviews instead"""
    with open(users) as f,\
         open(users.split(".")[0] + "_sample_" + str(size/1000) + ".csv", "w") as out:
        user_set = set(line.rstrip() for line in f)
        user_sample = sample(user_set, size)
        f.seek(0)
        for i, line in enumerate(f):
            if not i%10**4:
                print i
            if line.rstrip() in user_sample:
                out.write(line)

def sample_friends(users="users_sample_5.csv", friends="friends.csv"):
    """Only keep friends connections from users who are in the reviews"""
    with open(users) as u:
        user_set = set(line.rstrip() for line in u)

    print len(user_set)
    with open(friends) as f,\
         open(users.split(".")[0] + "_friends" + ".csv", "w") as out:
        
        for i, line in enumerate(f):
            if not i%10**6:
                print i
            u1, u2 = line.rstrip().split(";")
            if u1 in user_set and u2 in user_set:
                out.write(line)


if __name__ == "__main__":
    # sample_reviews(50, "50")
    # sample_users(1000)
    sample_friends(users="user_sample_50.csv")