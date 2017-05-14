class Movie:

    def __init__(self, title, link):
        self.title = title
        self.link = link
    
    def slug(self):
        lst = self.link.split("/")
        return lst[2]


    def __str__(self):
        return self.title.encode('utf-8')

    def __repr__(self):
        return self.title.encode('utf-8')
