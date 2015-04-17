
from functools import partial

# Create your score function, andd add it in get_score.
# Beware, you have to set your own threshold. Do not put a threshold too low.

 
def common_book_score(book_rating_1,  book_rating_2, book_set, threshold=100):
    """How many books have they in common?"""
    res = len(book_set)
    return res if res>threshold else None


def trivial_score(book_rating_1,  book_rating_2, book_set, threshold=1000):
    """Sum of ratings of both users on common books"""
    res = sum(book_rating_1[k]+book_rating_2[k] for k in book_set)
    return res if res>threshold else None


def rating_agreement(book_rating_1,  book_rating_2, book_set, threshold=0.7):
    """What is the fraction of books they have rated almost the same?"""
    # for book in book_set:
    #     print book_rating_1[book]
    if book_set:
        res  = sum([1 for book in book_set if abs(book_rating_1[book] - book_rating_2[book]) < 3]) / float(len(book_set))
        return res if res>threshold else None
    else:
        return None

def same_rating(book_rating_1,  book_rating_2, book_set, threshold=0.7):
    """If two users have given the same rating, the edge weight increases"""
    if book_set:
        res = 0
        for book in book_set:
            res += (5 - abs(book_rating_1[book] - book_rating_2[book]))**2
        res = 1. * res/len(book_set)
        return res if res>threshold else None
    return None

def same_rating_high(book_rating_1,  book_rating_2, book_set, threshold=0.7):
    """If two users have given the same rating, the edge weight increases
    Priviledge more the high ratings"""
    if book_set:
        res = 0
        for book in book_set:
            if abs(book_rating_1[book] - book_rating_2[book]) < 3:
                res += max(book_rating_1[book], book_rating_2[book])**3
        return res if res>threshold else None
    return None

def get_score(score_func, threshold):
    if score_func == "trivial":
        return partial(score_multi, score_func=partial(trivial_score, threshold=threshold))
    elif score_func == "common":
        return partial(score_multi, score_func=partial(common_book_score, threshold=threshold))
    elif score_func == "same_rating_2":
        return partial(score_multi, score_func=partial(rating_agreement, threshold=threshold))
    elif score_func == "same_rating":
        return partial(score_multi, score_func=partial(same_rating, threshold=threshold))
    elif score_func == "same_rating_high":
        return partial(score_multi, score_func=partial(same_rating_high, threshold=threshold))



def score_multi(edge, score_func=common_book_score):
    u, u_book_rating, u_books, v, v_book_rating, v_books = edge
    book_common = u_books.intersection(v_books)

    l = score_func(u_book_rating, u_book_rating, book_common)
    
    if l:
        return ";".join([str(i) for i in [u, v, l]])+"\n"
