from sample import sample_reviews
from reviews import Reviews
from user_graph import UserGraph

if __name__ == "__main__":

#   Correct scores function:
# trivial
# common
# same_rating_2
# same_rating
# same_rating_high

    scores = ["common", "same_rating_2", "same_rating_high"]
    threshold = [0, 0,  0]
    sample_filename = sample_reviews(3000, "3000_2")

    r = Reviews(sample_filename)
    for score, t in zip(scores, threshold):
        reviews_filenames = r.user_to_user(score=score, threshold=t, chunksize=30000, process=10)
        g = UserGraph(reviews_filenames)
        g.write_results()
