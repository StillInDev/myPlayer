from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class SongSelectionScreen(Screen):
    def __init__(self, song_list, **kwargs):
        super(SongSelectionScreen, self).__init__(**kwargs)

        self.song_list = song_list

        layout = BoxLayout(orientation='vertical')

        self.spot = 0

        self.song_layout = BoxLayout(orientation='vertical', size_hint_y=.85)
        for i in range(0, 5):
            song = self.song_list[self.spot]
            button_item = SongButton(text=song.name)
            self.song_layout.add_widget(button_item)
            self.spot += 1

        self.spot = 0

        layout.add_widget(self.song_layout)

        self.arrow_layout = BoxLayout(orientation='horizontal', size_hint_y=.15)
        left_arrow = BackArrow(text='Back')
        right_arrow = FrontArrow(text='Next')
        home_button = HomeButton(text='Home')
        self.arrow_layout.add_widget(left_arrow)
        self.arrow_layout.add_widget(home_button)
        self.arrow_layout.add_widget(right_arrow)
        layout.add_widget(self.arrow_layout)

        self.add_widget(layout)

    def update_shown_songs(self, switch):
        # Properly position 'spot'
        if switch > 0:      # -> Positive Number
            if self.spot + 10 >= len(self.song_list):      # -> Trying to go past the end
                self.spot = len(self.song_list) - 5
            else:
                self.spot += 5
        else:     # -> Negative Number
            if self.spot - 5 <= 0:     # -> Trying to go past the beginning
                self.spot = 0
            else:
                self.spot -= 5

        # Clear old widgets
        self.song_layout.clear_widgets()

        hold_spot = self.spot

        # Generate new widgets
        for i in range(0, 5):
            print("spot", self.spot)
            song = self.song_list[self.spot]
            print(song.name)
            button_item = SongButton(text=song.name)
            self.song_layout.add_widget(button_item)
            self.spot += 1

        self.spot = hold_spot


class SongButton(Button):
    def __init__(self, text, **kwargs):
        super(SongButton, self).__init__(**kwargs)
        self.text = text


class BackArrow(Button):
    def __init__(self, **kwargs):
        super(BackArrow, self).__init__(**kwargs)


class FrontArrow(Button):
    def __init__(self, **kwargs):
        super(FrontArrow, self).__init__(**kwargs)


class HomeButton(Button):
    def __init__(self, **kwargs):
        super(HomeButton, self).__init__(**kwargs)