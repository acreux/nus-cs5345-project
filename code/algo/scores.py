
from functools import partial



def common_book_score(book_rating_1,  book_rating_2, book_set, threshold=100):
    res = len(book_set)
    return res if res>threshold else None
        
def trivial_score(book_rating_1,  book_rating_2, book_set, threshold=1000):
    res = sum(book_rating_1[k]+book_rating_2[k] for k in book_set)
    return res if res>threshold else None
        
def get_score(score_func):
    if score_func == "trivial":
        return partial(score_multi, score_func=trivial_score)
    elif score_func == "common":
        return partial(score_multi, score_func=common_book_score)

def score_multi(edge, score_func=common_book_score):
    u, u_book_rating, u_books, v, v_book_rating, v_books = edge
    book_common = u_books.intersection(v_books)
    l = score_func(u_book_rating, v_book_rating, book_common)
    if l:
        return ";".join([str(i) for i in [u, v, l]])+"\n"