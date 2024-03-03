from googlesearch import search


class LinkGen:

  def __init__(self, user_input):
    self.user_input = user_input

  def generate_links(self):
    query_links = []
    for links in search(query=self.user_input,
                        tld="com",
                        lang="en",
                        num=3,
                        stop=3,
                        pause=2):
      query_links.append(links)
      print(self.user_input)

    return query_links

