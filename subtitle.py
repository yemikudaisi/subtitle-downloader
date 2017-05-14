class Subtitle:

    def __init__(self, title, link, language):
        self.title = title
        self.link = link
        self.language = language

    def __str__(self):
        return self.title.encode('utf-8')
