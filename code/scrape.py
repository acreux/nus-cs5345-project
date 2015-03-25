import goodreads


def rating_gen(client_id, client_secret, group_id):
    # c = goodreads.Client(client_id="C4VDKVDGbXYHqizAePFGg", client_secret="KDD6ZrT6820Z5vRlArDr8s0pI2PzlQVB9RY8SLm08")
    c = goodreads.Client(client_id=client_id, client_secret=client_secret)
    c.authenticate()
    print "authenticated"
    all_members = c.all_group_members(group_id)
    for member in all_members:
        member_id = member['id']['#text']
        for review in c.review_list_all(member_id):
            # print review
            yield member_id, review['book']['id']['#text'], review['rating']


def scrape_group(client_id, client_secret, group_id, filename):
    with open(filename, 'a') as f:
        for u, b, r in rating_gen(client_id, client_secret, group_id):
            f.write(';'.join([u, b, r]) + '\n')

