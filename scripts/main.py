import os

import pygame
import sounddevice
import soundfile
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

from myPlayer.myPlayer.scripts.songs import Song

# Holds all songs
song_list = []

# Variables
SAMPLE_RATE = 44100 * 1.0925  # -> Standard is 44.1 kHz
# Rate for Fair Trade = 44100*1.0925
index = 0

'''#---------------SCREENS---------------#'''
class MenuScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass

class LibraryScreen(Screen):
    def __init__(self, **kwargs):
        super(LibraryScreen, self).__init__(**kwargs)

        for song in song_list:
            button_item = SongButton(text=song.name)
            self.add_widget(button_item)

class ButtonListItem(BoxLayout):
    def __init__(self, text, **kwargs):
        super(ButtonListItem, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.button = Button(text=text)
        self.add_widget(self.button)

        self.button.bind(on_release=self.button_click)

    def button_click(self, instance):
        print(f"clicked: {instance.text}")

class SongButton(Button):
    def __init__(self, text, **kwargs):
        super(SongButton, self).__init__(**kwargs)

class PlayScreen(Screen):
    # SO WE NEED TO KEEP TRACK OF WHERE YOU LEFT OFF IN LAST PLAYLIST
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        self.start_time = None
        self.playing = False  # Track play/pause state
        self.played = False
        self.playback_data = None
        self.playback_position = 0
        self.dex = 0
        self.song_list = song_list
        self.reload = True

    def skip_song(self):
        # If you reach the end of the song_list
        self.reload = True
        if len(self.song_list) <= self.dex + 1:
            self.dex = 0
        # Just add one
        else:
            self.dex += 1
        self.play_song()

    def back_song(self):
        self.reload = True
        if 0 >= self.dex:
            self.dex = len(self.song_list) - 1
        # Just add one
        else:
            self.dex -= 1
        self.play_song()

    def load_song(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.song_list[self.dex].path)

        # Load audio data for precise playback control
        self.playback_data, _ = soundfile.read(self.song_list[self.dex].path, dtype='int16')

    def play_song(self, select=None):
        if select is not None:
            self.dex = select

        print('start', self.start_time)
        if not self.playing:
            # MIGHT HAVE AN ISSUE WITH A CHANGE IN SONG
            self.playing = True
            self.ids.play_button.text = 'Pause'
            self.ids.play_button.background_color = 1, 0, 0, 1  # Red for pause state

            if self.playback_data is None or self.reload:
                self.reload = False
                self.load_song()

            self.start_time = time.time() - self.playback_position / SAMPLE_RATE
            sounddevice.play(self.playback_data[self.playback_position:], SAMPLE_RATE)
        else:
            self.playing = False
            self.ids.play_button.text = 'Play'
            self.ids.play_button.background_color = 0, 1, 0, 1  # Green for play state

            elapsed_time = time.time() - self.start_time
            self.playback_position += int(elapsed_time * SAMPLE_RATE)  # Convert to samples
            sounddevice.stop()

    def update_time(self):
        if self.playing:
            elapsed_time = time.time() - self.start_time
            self.playback_position += int(elapsed_time * SAMPLE_RATE)  # Convert to samples
            self.start_time = time.time()

    def on_playback_position(self, dt):
        self.update_time()
        if self.playing:
            print("Elapsed Time:", self.playback_position / SAMPLE_RATE)


# Main class
class MyApp(App):
    # Starts loading the application

    def build(self):
        build_song_list(self)
        print(song_list)

        self.playMusicScreen = PlayScreen(name='playMusicScreen')

        # Loads screen
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(self.playMusicScreen)
        sm.add_widget(LibraryScreen(name='library'))

        return sm


def build_song_list(self):
    # Get song folder path
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    song_folder_path = os.path.join(parent_directory, 'songs')

    # Fill song_list with all songs
    for filename in os.listdir(song_folder_path):
        if filename.endswith('.mp3'):
            song_path = os.path.join(song_folder_path, filename)
            song = Song(text=song_path)
            song_list.append(song)



if __name__ == '__main__':
    MyApp().run()