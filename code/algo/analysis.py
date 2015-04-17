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

    # scores = ["trivial", "common", "same_rating_2", "same_rating", "same_rating_high"]
    # threshold = [0, 0, 0, 0, 0]
    # sample_filename = sample_reviews(2600, "2600_1")

    # r = Reviews(sample_filename)
    # for score, t in zip(scores, threshold):
    #     reviews_filenames = r.user_to_user(score=score, threshold=0, chunksize=50000, process=10)
    #     g = UserGraph(reviews_filenames)
    #     g.write_results()
    files = ["edges_trivial_sample_2600_1.csv", "edges_trivial_sample_2600_1_timer.txt", "edges_common_sample_2600_1.csv", "edges_common_sample_2600_1_timer.txt", "edges_same-rating-2_sample_2600_1.csv", "edges_same-rating-2_sample_2600_1_timer.txt", "edges_same-rating_sample_2600_1.csv", "edges_same-rating_sample_2600_1_timer.txt", "edges_same-rating-high_sample_2600_1.csv", "edges_same-rating-high_sample_2600_1_timer.txt"]
    files = ["edges_common_50.csv"]
    for f in files:
        g = UserGraph(f)
        g.write_results()