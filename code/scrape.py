from pygoodreads.base import GoodreadsSession
import time, random

class Scrape(object):

    FILENAME = "test1"

    def __init__(self):
        self.session = GoodreadsSession(config_file="goodreads.cfg")
        self.session.connect()
        self.user_already_scraped = set([])

    def rating_gen(self, group_id):
        all_members = self.session.all_group_members(group_id)
        for member in all_members:
            # 1 out 10, we dont move for 1 minute
            if random.random() > 1:
                print "sleep"
                time.sleep(60)
            member_id = member['id']['#text']
            if member_id in self.user_already_scraped:
                print member_id, " already scraped"
                continue
            else:
                self.user_already_scraped.add(member_id)

            review_count = 0
            for review in self.session.reviews_all(member_id):
                review_count += 1
                yield member_id, review['book']['id']['#text'], review['rating']
            if review_count == 0:
                yield member_id, "0000000000", "0000"


    def scrape_group(self, group_id):
        lines_count = 0
        # buffering=1 means flush at each line
        with open(self.FILENAME, 'a', buffering=1) as f:
            if lines_count > 10**9:
                return
            for u, b, r in self.rating_gen(group_id):
                lines_count += 1
                f.write(';'.join([u, b, r]) + '\n')

    def user_already_scraped(self):
        with open(self.FILENAME) as f:
            self.user_already_scraped = set((line.split(";")[0] for line in f.readlines()))

if __name__ == "__main__":
    superman = Scrape()
    superman.scrape_group(26989)