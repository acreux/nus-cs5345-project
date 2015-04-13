
from functools import partial

# Create your score function, andd add it in get_score.
#  Beware, you have to set your own threshold. Do not put a threshold too low.

 
def common_book_score(book_rating_1,  book_rating_2, book_set, threshold=100):
    """book_rating_1 = book to """
    res = len(book_set)
    return res if res>threshold else None
        
def trivial_score(book_rating_1,  book_rating_2, book_set, threshold=1000):
    res = sum(book_rating_1[k]+book_rating_2[k] for k in book_set)
    return res if res>threshold else None
        

def rating_agreement(book_rating_1,  book_rating_2, book_set, threshold=0.7):
    for book in book_set:
        print book_rating_1[book]
   # res  = sum(1 for book in book_set if abs(book_rating_1[book] - book_rating_2[book]) < 2) / float(len(book_set))
   # return res if res>threshold else None
	

def get_score(score_func, threshold):
    if score_func == "trivial":
        return partial(score_multi, score_func=partial(trivial_score, threshold=threshold))
    elif score_func == "common":
        return partial(score_multi, score_func=partial(common_book_score, threshold=threshold))
    elif score_func == "rating":
        return partial(score_multi, score_func=partial(rating_agreement, threshold=threshold))

def score_multi(edge, score_func=common_book_score):
    u, u_book_rating, u_books, v, v_book_rating, v_books = edge
    book_common = u_books.intersection(v_books)

    u_b_r = { k : int(v) for k, v in u_book_rating }
    v_b_r = { k : int(v) for k, v in v_book_rating }
    l = score_func(u_b_r, v_b_r, book_common)
    
    if l:
        return ";".join([str(i) for i in [u, v, l]])+"\n"
