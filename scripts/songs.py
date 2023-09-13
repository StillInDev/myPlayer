class Song():
    def __init__(self, text, sample_rate = 44100, **kwargs):
        super(Song, self).__init__(**kwargs)
        print('t', text)

        parts = text.split('-')
        self.path = text
        print('p', len(parts))

        print()
        self.name = parts[1].strip()

        self.sample_rate = sample_rate
