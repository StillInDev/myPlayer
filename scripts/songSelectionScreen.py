from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class SongSelectionScreen(Screen):
    def __init__(self, song_list, playlist_list, **kwargs):
        super(SongSelectionScreen, self).__init__(**kwargs)

        self.song_list = song_list
        self.playlist_list = playlist_list

        self.base_layout = BoxLayout(orientation='vertical')

        self.song_spot = 0     # Variable to hold the song spot for the arrow clicking
        self.p_spot = 0     # Variable to hold the playlist spot for the arrow clicking

        self.playlist_clicked = False     # Variable is used in clean up to choose a method

        # I am going to create a base_layout and essentially replace it when a playlist is selected
        # The playlist layout is going to be called base_playlist_layout
        # The song layout = base_song_layout

        self.base_playlist_layout = BoxLayout(orientation='vertical')

        self.playlist_layout = BoxLayout(orientation='vertical', size_hint_y=0.85)
        for i in range(0, 5):
            if self.p_spot >= len(self.playlist_list):
                break
            playlist = self.playlist_list[self.p_spot]
            if playlist is None:
                break
            button_item = playlistButton(text=playlist.name)
            self.playlist_layout.add_widget(button_item)
            self.p_spot += 1

        self.p_spot = 0

        self.base_playlist_layout.add_widget(self.playlist_layout)

        self.p_arrow_layout = BoxLayout(orientation='horizontal', size_hint_y=.15)
        left_arrow = playlistBackArrow(text='Back')
        right_arrow = playlistFrontArrow(text='Next')
        home_button = HomeButton(text='Home')
        self.p_arrow_layout.add_widget(left_arrow)
        self.p_arrow_layout.add_widget(home_button)
        self.p_arrow_layout.add_widget(right_arrow)

        # Add the arrow_layout to the base_song_layout
        self.base_playlist_layout.add_widget(self.p_arrow_layout)

        # ---------------Define Base_Song_Layout---------------#

        self.base_song_layout = BoxLayout(orientation='vertical')

        self.song_layout = BoxLayout(orientation='vertical', size_hint_y=.85)
        for i in range(0, 5):
            song = self.song_list[self.song_spot]
            button_item = SongButton(text=song.name)
            self.song_layout.add_widget(button_item)
            self.song_spot += 1

        self.song_spot = 0

        self.base_song_layout.add_widget(self.song_layout)

        self.arrow_layout = BoxLayout(orientation='horizontal', size_hint_y=.15)
        left_arrow = SongBackArrow(text='Back')
        right_arrow = SongFrontArrow(text='Next')
        home_button = HomeButton(text='Home')
        self.arrow_layout.add_widget(left_arrow)
        self.arrow_layout.add_widget(home_button)
        self.arrow_layout.add_widget(right_arrow)

        # Add the arrow_layout to the base_song_layout
        self.base_song_layout.add_widget(self.arrow_layout)

        # Add the base_playlist_layout to print
        self.base_layout.add_widget(self.base_playlist_layout)
        self.add_widget(self.base_layout)

    def select_playlist(self, name):
        self.playlist_clicked = True
        playlist = self.find_playlist(name)
        print('pn', playlist.name)
        self.song_list = playlist.songs

        self.base_layout.remove_widget(self.base_playlist_layout)
        self.base_layout.add_widget(self.base_song_layout)

        self.update_shown_songs(-1)

    def find_playlist(self, title):
        for playlist in self.playlist_list:
            if playlist.name == title:  # Assuming the Playlist class has a 'name' attribute
                return playlist

    def update_shown_songs(self, switch):
        # Properly position 'spot'
        if switch > 0:  # -> Positive Number
            if self.song_spot + 10 >= len(self.song_list):  # -> Trying to go past the end
                self.song_spot = len(self.song_list) - 5
                if self.song_spot < 0:
                    self.song_spot = 0
            else:
                self.song_spot += 5
        else:  # -> Negative Number
            if self.song_spot - 5 <= 0:  # -> Trying to go past the beginning
                self.song_spot = 0
            else:
                self.song_spot -= 5

        # Clear old widgets
        self.song_layout.clear_widgets()

        hold_spot = self.song_spot

        # Generate new widgets
        for i in range(0, 5):
            print("spot", self.song_spot)
            if i >= len(self.song_list):
                break
            song = self.song_list[self.song_spot]
            print(song.name)
            button_item = SongButton(text=song.name)
            self.song_layout.add_widget(button_item)
            self.song_spot += 1

        self.song_spot = hold_spot

    def update_shown_playlists(self, switch):
        # Properly position 'spot'
        if switch > 0:  # -> Positive Number
            if self.p_spot + 10 >= len(self.playlist_list):  # -> Trying to go past the end
                self.p_spot = len(self.playlist_list) - 5
                if self.p_spot < 0:
                    self.p_spot = 0
            else:
                self.p_spot += 5
        else:  # -> Negative Number
            if self.p_spot - 5 <= 0:  # -> Trying to go past the beginning
                self.p_spot = 0
            else:
                self.p_spot -= 5

        # Clear old widgets
        self.playlist_layout.clear_widgets()

        hold_spot = self.p_spot

        # Generate new widgets
        for i in range(0, 5):
            if i >= len(self.playlist_list):
                break
            playlist = self.playlist_list[self.p_spot]
            button_item = playlistButton(text=playlist.name)
            self.playlist_layout.add_widget(button_item)
            self.p_spot += 1

        self.p_spot = hold_spot

    def reset(self):
        if self.playlist_clicked:
            self.base_layout.remove_widget(self.base_song_layout)
            self.base_layout.add_widget(self.base_playlist_layout)
            self.playlist_clicked = False


class playlistButton(Button):
    def __init__(self, text, **kwargs):
        super(playlistButton, self).__init__(**kwargs)
        self.text = text


class playlistBackArrow(Button):
    def __init__(self, **kwargs):
        super(playlistBackArrow, self).__init__(**kwargs)


class playlistFrontArrow(Button):
    def __init__(self, **kwargs):
        super(playlistFrontArrow, self).__init__(**kwargs)
        self.background_normal = 'myPlayer/images/right-arrow.png'
        self.border = (0,0,0,0)

class SongButton(Button):
    def __init__(self, text, **kwargs):
        super(SongButton, self).__init__(**kwargs)
        self.text = text


class SongBackArrow(Button):
    def __init__(self, **kwargs):
        super(SongBackArrow, self).__init__(**kwargs)


class SongFrontArrow(Button):
    def __init__(self, **kwargs):
        super(SongFrontArrow, self).__init__(**kwargs)


class HomeButton(Button):
    def __init__(self, **kwargs):
        super(HomeButton, self).__init__(**kwargs)
