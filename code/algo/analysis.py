from sample import sample_reviews
from reviews import Reviews
from user_graph import UserGraph

if __name__ == "__main__":

#   Correct scores function:
#     trivial
#     common
#     same_rating_2

    
    # sample_filename = sample_reviews(2000, "2000_1")

    # r = Reviews(sample_filename)

    # reviews_filenames1 = r.user_to_user(score="trivial", threshold=0, chunksize=50000, process=10)
    # reviews_filenames2 = r.user_to_user(score="same_rating_2", threshold=0, chunksize=50000, process=10)
    # reviews_filenames3 = r.user_to_user(score="common", threshold=0, chunksize=50000, process=10)

    g = UserGraph(reviews_filenames1)
    g.write_results()
    g = UserGraph(reviews_filenames2)
    g.write_results()
    g = UserGraph(reviews_filenames3)
    g.write_results()
