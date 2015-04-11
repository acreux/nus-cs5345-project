from random import sample

def sample_reviews(size=10**4, reviews="reviews_all.csv"):
    with open(reviews) as f,\
         open(reviews.split(".")[0] + "_sample_" + str(size/1000) + ".csv", "w") as out:
        user_set = set(int(line.rstrip().split(";")[1]) for line in f)
        user_sample = sample(user_set, size)
        f.seek(0)
        for i, line in enumerate(f):
            if not i%10**4:
                print i
            if int(line.rstrip().split(";")[1]) in user_sample:
                out.write(line)

def sample_users(size=10**4, users="users.csv"):
    with open(users) as f,\
         open(users.split(".")[0] + "_sample_" + str(size/1000) + ".csv", "w") as out:
        user_set = set(int(line.rstrip()) for line in f)
        user_sample = sample(user_set, size)
        f.seek(0)
        for i, line in enumerate(f):
            if not i%10**4:
                print i
            ifint(line.rstrip()) in user_sample:
                out.write(line)

def sample_friends(reviews="reviews_all_10.csv", friends="friends.csv"):
    """Only keep friends connections from users who are in the reviews"""
    with open(reviews) as f,\
         open(reviews.split(".")[0] + "_sample_friends_" + ".csv", "w") as out:
        user_set = set(line.rstrip().split(";")[1] for line in f)
        f.seek(0)
        for i, line in enumerate(f):
            if not i%10**6:
                print i
            u1, u2 = line.rstrip().split(";")
            if u1 in user_set and u2 in user_set:
                out.write(line)


if __name__ == "__main__":
    # sample_reviews()
    sample_users()