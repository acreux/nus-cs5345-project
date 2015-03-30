from __future__ import with_statement
import time, random, pickle
from pygoodreads import GoodreadsSession, ProfilePrivateException, NotFoundProfileException
import os


class Scrape(object):

    FOLDER = 'data'

    REGISTERED = "scraped"
    FRIENDS = "friends"
    NOT_FOUND = "not_found"
    FORBIDDEN = "forbidden"
    EMPTY = "empty"

    def __init__(self, group_id, min_page=1, max_page=10**9):
        self.session = GoodreadsSession(config_file="goodreads.cfg")
        self.session.connect()
        self._not_found = None
        self._forbidden = None
        self._registered = None
        self._empty = None
        self.min_page = min_page
        self.max_page = max_page
        self.group_id = group_id
        generate_file_name = lambda prefix: os.path.join(self.FOLDER,
                                                         str(self.group_id),
                                                         "_".join([prefix,
                                                                   str(self.group_id),
                                                                   str(self.min_page),
                                                                   str(self.max_page)]))
        # generate_file_name = lambda prefix: "_".join([prefix])

        # From previous scraping
        self.not_found_basic = os.path.join(self.FOLDER, self.NOT_FOUND)
        self.forbidden_basic = os.path.join(self.FOLDER, self.FORBIDDEN)
        self.empty_basic = os.path.join(self.FOLDER, self.EMPTY)

        # New files created
        self.not_found_file = generate_file_name(self.NOT_FOUND)
        self.forbidden_file = generate_file_name(self.FORBIDDEN)
        self.registered_file = generate_file_name(self.REGISTERED)
        self.empty_file = generate_file_name(self.EMPTY)
        self.friends_file = generate_file_name(self.FRIENDS)

    def rating_gen(self):
        all_members = self.session.group_members_all(self.group_id,
                                                     self.min_page,
                                                     self.max_page)
        for member in all_members:
            # 1 out 10, we don't move for 1 minute
            # if random.random() > 1:
            #     print "sleep"
            #     time.sleep(60)

            member_id = member['id']['#text']
            is_visited = self.is_visited(str(member_id))
            if is_visited:
                print member_id, "already ", is_visited, " ", self.min_page
                continue

            try:
                review_count = 0
                for review in self.session.reviews_all(member_id):
                    yield "good", member_id, review['book']['id']['#text'], review['rating']
                    review_count += 1
                if review_count == 0:
                    yield "empty", member_id, "", ""
                    print member_id, " empty", " ", self.min_page
                else:
                    self.scrape_friends(member_id)
                    self.registered.add(member_id)
                    print member_id, " visited", " ", self.min_page

            except ProfilePrivateException:
                self.forbidden.add(member_id)
                yield "forbidden", member_id, "", ""
                print member_id, " forbidden", " ", self.min_page

            except NotFoundProfileException:
                self.not_found.add(member_id)
                yield "not_found", member_id, "", ""
                print member_id, " not_found", " ", self.min_page
            # except Exception as e:
            #     print e
            #     print "Exception raised for ", member_id

    def friends_gen(self, user_id):
        all_friends = self.session.friends_all(user_id)
        try:
            for friend in all_friends:
                yield friend['id'], friend['reviews_count'], friend['friends_count'], user_id
        except ProfilePrivateException:
            self.forbidden.add(member_id)
        except NotFoundProfileException:
            self.not_found.add(member_id)

    def scrape_friends(self, user_id):
        with open(self.friends_file, "a", buffering=1) as f:
            for line in self.friends_gen(user_id):
                f.write(";".join(line) + "\n")

    def scrape(self):
        lines_count = 0
        # buffering=1 means flush at each line
        with open(self.registered_file, "a", buffering=1) as scraped,\
             open(self.not_found_file, "a", buffering=0) as not_found,\
             open(self.forbidden_file, "a", buffering=0) as forbidden,\
             open(self.empty_file, "a", buffering=0) as empty:
            file_dict = {
                "good": scraped,
                "not_found": not_found,
                "empty": empty,
                "forbidden": forbidden}
            for status, user, book, rating in self.rating_gen():
                f = file_dict[status]
                if status == "good":
                    f.write(';'.join([user, book, rating]) + '\n')
                else:
                    f.write(user + '\n')
        print "Scrape: ", self.min_page, "-", self.max_page, " fini"

    @property
    def registered(self):
        """Member currently stored in file"""
        if not self._registered:
            try:
                with open(self.registered_file) as f:
                    self._registered = set((line.split(";")[0] for line in f.readlines()))
            except IOError:
                self._registered = set([])
        return self._registered

    def read_set(self, filename):
        try:
            with open(filename) as f:
                lines = (line.rstrip() for line in f)
                return set(lines)
        except IOError:
            return set([])

    @property
    def forbidden(self):
        if not self._forbidden:
            self._forbidden = self.read_set(self.forbidden_basic) | self.read_set(self.forbidden_file)
        return self._forbidden

    @property
    def empty(self):
        if not self._empty:
            self._empty = self.read_set(self.empty_basic) | self.read_set(self.empty_file)
        return self._empty

    @property
    def not_found(self):
        if not self._not_found:
            self._not_found = self.read_set(self.not_found_basic) | self.read_set(self.not_found_file)
        return self._not_found

    def is_visited(self, user_id):
        if user_id in self.registered:
            return "registered"
        elif user_id in self.forbidden:
            return "forbidden"
        elif user_id in self.empty:
            return "empty"
        elif user_id in self.not_found:
            return "not_found"
        else:
            return None


if __name__ == "__main__":
    # for i in range(100):
    #     superman = Scrape(group_id=26989, min_page=329 + i*20, max_page=329 + (i+1)*20 - 1)
    #     superman.scrape()
    superman = Scrape(group_id=26989, min_page=660, max_page=666)
    # print len(superman.not_found)
    print len(superman.forbidden)
    # print len(superman.empty)
    # superman.scrape()
