class Song():
    def __init__(self, text, sample_rate = 44100, **kwargs):
        super(Song, self).__init__(**kwargs)
        parts = text.split('-')
        name_part = parts[1].split('.')
        self.path = text
        self.name = name_part[0].strip()

        self.sample_rate = sample_rate
