import multiprocessing
from tor import Tor
from scrape import Scrape


class Multiprocessing(object):

    def __init__(self, func):
        self.pool = multiprocessing.Pool()
        self.func = func

    def do(self, iterable):
        self.results = self.pool.map(self.func, iterable)
        self.pool.close()
        self.pool.join()


def scrape(scrape_params):
    group_id = scrape_params['group_id']
    min_page = scrape_params['min_page']
    max_page = scrape_params['max_page']
    superman = Scrape(group_id, min_page=min_page, max_page=max_page)
    superman.scrape()


if __name__ == "__main__":
    min_page = 667
    page_batch = 2
    with Tor(socks_port=7000) as t:
        iterable = [
            {
                "group_id":26989,
                "min_page":min_page + page_batch*i+1,
                "max_page":min_page + page_batch*(i+1)}
            for i in range(16)]
        a = Multiprocessing(scrape)
        a.do(iterable)

    # scrape({
    #         "group_id":26989,
    #         "min_page":min_page + 50+1,
    #         "max_page":min_page + 50*(1+1)})
