import multiprocessing
from tor import Tor
from scrape import Scrape, UserScrape


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


def scrape_files(file_id):
    print "start " + str(file_id)
    superman = UserScrape(file_id)
    superman.scrape()
    # try:
    #     superman.scrape_friends()
    # except Exception as e:
    #     print e



if __name__ == "__main__":

    scrape_files(946)

    # page_batch = 20
    # group_id = 390
    # max_iter = 0
    
    # min_page = 1
    # max_page = min_page + page_batch*(max_iter+1)-1
    # cpt = 0
    # while min_page<578:
    #     cpt += 1
    #     print cpt, max_page
        
        # with Tor(socks_port=7000) as t:
        #     iterable = [
        #         {"group_id":group_id,
        #          "min_page":min_page + page_batch*i,
        #          "max_page":min_page + page_batch*(i+1)-1}
        #         for i in range(max_iter+1)]
        #     a = Multiprocessing(scrape)
        #     a.do(iterable)
        # print cpt, max_page
        
        # iterable = [=
        #     {"group_id":group_id,
        #      "min_page":min_page + page_batch*i,
        #      "max_page":min_page + page_batch*(i+1)-1}
        #     for i in range(max_iter+1)]
        # a = Multiprocessing(scrape)
        # a.do(iterable)

        # scrape({"group_id":group_id,
        #      "min_page":min_page,
        #      "max_page":min_page + page_batch-1})
        # min_page = max_page+1
        # max_page = min_page + page_bacdtch*(max_iter+1)-1


    # for i in range(700, 960, 50):
    #     iterable = range(i, i+49)
    #     a = Multiprocessing(scrape_files)
    #     a.do(iterable)
    # scrape_files(955)

    # scrape({"group_id":group_id,
    #         "min_page":min_page + 50+1,
    #         "max_page":min_page + 50*(1+1)})
    
    # print max_page
    # superman = Scrape(group_id, min_page=min_page, max_page=min_page+page_batch)
    # print str(3770173) in superman.not_found
    # # print superman.forbidden