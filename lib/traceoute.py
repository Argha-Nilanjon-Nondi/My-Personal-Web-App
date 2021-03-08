import builtwith

class Traceoute:
    def __init__(self, url):
        self.url = url

    @property
    def find(self):
        return builtwith.parse(self.url)
