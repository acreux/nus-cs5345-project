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

    def __init__(self):
        self.session = GoodreadsSession(config_file="goodreads.cfg")
        self.session.connect()
        self._not_found = None
        self._forbidden = None
        self._registered = None
        self._empty = None

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

    def read_set(self, filename):
        try:
            with open(filename) as f:
                return set((line.rstrip() for line in f))
        except IOError:
            return set([])

    @property
    def forbidden(self):
        if not self._forbidden:
            self._forbidden = self.read_set(self.forbidden_basic) | self.read_set(self.forbidden_file)
        return self._forbidden


class GroupScrape(Scrape):

    def __init__(self, group_id, min_page=1, max_page=10**9):
        Scrape.__init__(self)
        self.min_page = min_page
        self.max_page = max_page
        self.group_id = group_id
        generate_file_name = lambda prefix: os.path.join(self.FOLDER,
                                                         str(self.group_id),
                                                         "_".join([prefix,
                                                                   str(self.group_id),
                                                                   str(self.min_page),
                                                                   str(self.max_page)]))


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

    def member_reviews(self, member_id):
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

    def member_gen(self):
        all_members = self.session.group_members_all(self.group_id,
                                                     self.min_page,
                                                     self.max_page)
        for member in all_members:
            # 1 out 10, we don't move for 1 minute
            # if random.random() > 1:
            #     print "sleep"
            #     time.sleep(60)

            # yield member_id
            yield member['id']['#text']

    def rating_gen(self, user_id_gen):
        for member_id in user_id_gen:
            is_visited = self.is_visited(str(member_id))
            if is_visited:
                print member_id, "already ", is_visited, " ", self.min_page
                continue

            try:
                for r in self.member_reviews(member_id):
                    yield r
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

    def scrape(self):
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
            for status, user, book, rating in self.rating_gen(user_id_gen):
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


class UserScrape(Scrape):

    FOLDER = "data/next_26989"
    FILE = "users_{}"

    def __init__(self, user_file_id):
        Scrape.__init__(self)
        self.user_file = self.FILE.format(str(user_file_id).zfill(3))
        self.input_file = os.path.join(self.FOLDER, self.user_file)
        self.output_file = os.path.join(self.FOLDER, self.user_file + "_output")
        self.forbidden_file = os.path.join(self.FOLDER, self.user_file + "_forbidden")
        self.not_found_file = os.path.join(self.FOLDER, self.user_file + "_not_found")
        
        self.friends_file = os.path.join(self.FOLDER, self.user_file + "_friends")
        
        self._registered = None
        self._forbidden = None
        self._not_found = None
        self._friends_registered = None

        self.forbidden_basic = os.path.join(self.FOLDER, self.FORBIDDEN)
        self.not_found_basic = os.path.join(self.FOLDER, self.NOT_FOUND)

    def member_gen(self):
        with open(self.input_file) as f:
            for line in f:
                yield line.rstrip()

    def member_reviews(self, member_id):
        empty = True
        for review in self.session.reviews_all(member_id):
            empty = False
            yield "good", member_id, review['book']['id']['#text'], review['rating']
        if not empty:
            print member_id, " done"
        else:
            print member_id, " empty"

    def rating_gen(self, user_id_gen):
        for member_id in user_id_gen:
            is_visited = self.is_visited(str(member_id))
            if is_visited:
                print member_id, "already ", is_visited, " "
                continue
            try:
                for r in self.member_reviews(member_id):
                    yield r
            except ProfilePrivateException:
                yield "forbidden", member_id, "XXX", "XXX"
                print member_id, " forbidden"
            except NotFoundProfileException:
                yield "not_found", member_id, "XXX", "XXX"
                print member_id, " not_found"

    def scrape(self):
        # buffering=1 means flush at each line
        with open(self.output_file, "a", buffering=1) as scraped,\
             open(self.forbidden_file, "a", buffering=1) as forbidden,\
             open(self.not_found_file, "a", buffering=1) as not_found:
            for status, user, book, rating in self.rating_gen(self.member_gen()):
                if "good" in status:
                    scraped.write(';'.join([user, book, rating]) + '\n')
                elif "forbidden" in status:
                    forbidden.write(user + '\n')
                elif "not" in status:
                    not_found.write(user + '\n')
                else:
                    raise Exception(status + " unknown")

    def friends_gen(self, user_id_gen):
        for user_id in user_id_gen:
            is_visited = self.is_visited_friends(str(user_id))
            if is_visited:
                # print user_id, "already ", is_visited
                continue

            all_friends = self.session.friends_all(user_id)
            try:
                for friend in all_friends:
                    yield user_id, friend['id'], friend['friends_count'], friend['reviews_count']
            except ProfilePrivateException:
                self.forbidden.add(user_id)
            except NotFoundProfileException:
                self.not_found.add(user_id)

    def scrape_friends(self):
        # buffering=1 means flush at each line
        with open(self.friends_file, "a", buffering=1) as friends_file:
            for line in self.friends_gen(self.member_gen()):
                friends_file.write(";".join(line) + "\n")

    @property
    def registered(self):
        """Member currently stored in file"""
        if not self._registered:
            try:
                with open(self.output_file) as f:
                    self._registered = set((line.split(";")[0] for line in f.readlines()))
            except IOError:
                self._registered = set([])
        return self._registered

    def is_visited(self, user_id):
        if user_id in self.registered:
            return "registered"
        else:
            return None

    def is_visited_friends(self, user_id):
        if user_id in self.friends_registered:
            return "friends registered"
        else:
            return None

    @property
    def friends_registered(self):
        """Friends already retrieved currently stored in file"""
        if not self._friends_registered:
            try:
                with open(self.friends_file) as f:
                    self._friends_registered = set((line.split(";")[0] for line in f.readlines()))
            except IOError:
                self._friends_registered = set([])
        return self._friends_registered

    @property
    def forbidden(self):
        if not self._forbidden:
            self._forbidden = self.read_set(self.forbidden_basic) | self.read_set(self.forbidden_file)
        return self._forbidden

    @property
    def not_found(self):
        if not self._not_found:
            self._not_found = self.read_set(self.not_found_basic) | self.read_set(self.not_found_file)
        return self._not_found


if __name__ == "__main__":
    pass
    # for i in range(1, 101):
    # #     superman = Scrape(group_id=26989, min_page=329 + i*20, max_page=329 + (i+1)*20 - 1)
    # #     superman.scrape()
    # for i in range(70, 101):
    #     superman = UserScrape(i)
    #     superman.scrape_friends()
    superman = UserScrape(1)
    superman.scrape_friends()