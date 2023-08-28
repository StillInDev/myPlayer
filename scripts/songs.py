class Song():
    def __init__(self, text, **kwargs):
        super(Song, self).__init__(**kwargs)
        parts = text.split('-')
        self.path = text
        self.name = parts[1].strip()
