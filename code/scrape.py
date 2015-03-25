from pygoodreads.base import GoodreadsSession

class Scrape(object):

    def __init__(self):
        self.session = GoodreadsSession(config_file="goodreads.cfg")
        self.session.connect()

    def rating_gen(self, group_id):
        all_members = self.session.all_group_members(group_id)
        for member in all_members:
            member_id = member['id']['#text']
            for review in self.session.review_list_all(member_id):
                yield member_id, review['book']['id']['#text'], review['rating']


    def scrape_group(self, group_id, filename):
        # buffering=1 means flush at each line
        with open(filename, 'a', buffering=1) as f:
            for u, b, r in self.rating_gen(group_id):
                f.write(';'.join([u, b, r]) + '\n')

if __name__ == "__main__":
    superman = Scrape()
    superman.scrape_group(26989, "test1")