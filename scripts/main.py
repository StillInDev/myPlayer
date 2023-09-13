import os

import pygame
import sounddevice
import soundfile
import time

from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView

from kivy.uix.popup import Popup
from kivy.properties import StringProperty

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from pydub import AudioSegment

from myPlayer.scripts.playlists import Playlist
from myPlayer.scripts.playscreen import *
from myPlayer.scripts.songs import Song
from myPlayer.scripts.songSelectionScreen import SongSelectionScreen

from kivy.lang import Builder

# Combines all the .kv files specified
Builder.load_file('menuScreen.kv')
Builder.load_file('playScreen.kv')
Builder.load_file('songSelectionScreen.kv')

# Holds all allSongs
all_song_list = []
playlist_pages = []

# Variables
SAMPLE_RATE = 44100 * 1.0925  # -> Standard is 44.1 kHz
# Rate for Fair Trade = 44100*1.0925
index = 0

'''#---------------SCREENS---------------#'''


class MenuScreen(Screen):
    pass


# Main class
class MyApp(App):
    # Starts loading the application

    def build(self):
        all_song_list = build_song_list('allSongs', self)
        print(all_song_list)

        playlist_pages = build_playlist_pages(self)
        print(playlist_pages)

        self.playMusicScreen = PlayScreen(name='playMusicScreen', song_list=all_song_list, sample_rate=SAMPLE_RATE)
        self.songSelectionScreen = SongSelectionScreen(name='playlist', song_list=all_song_list, playlist_list=playlist_pages)
        self.menuScreen = MenuScreen(name='menuScreen')

        # Loads screen
        sm = ScreenManager()
        sm.add_widget(self.menuScreen)
        sm.add_widget(self.playMusicScreen)
        sm.add_widget(self.songSelectionScreen)

        return sm


def build_song_list(folder_name, self):
    song_list = []
    # Get song folder path
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    song_folder_path = os.path.join(parent_directory,'zongs', str(folder_name))

    # Fill song_list with all allSongs
    for filename in os.listdir(song_folder_path):
        if filename.endswith('.mp3'):
            song_path = os.path.join(song_folder_path, filename)
            song = Song(text=song_path)
            song_list.append(song)

    return song_list


def build_playlist_pages(self):
    # Get playlist location
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    playlist_pages_path = os.path.join(parent_directory, 'zongs')

    library = []
    for folder_name in os.listdir(playlist_pages_path):
        # print("folder", folder_name)
        full_folder_path = os.path.join(playlist_pages_path, folder_name)
        if os.path.isdir(full_folder_path):
            songs_in_folder = build_song_list(folder_name, self)
            playlist = Playlist(name=folder_name, song_list=songs_in_folder)
            library.append(playlist)

    print("playlist", library)

    return library


if __name__ == '__main__':
    MyApp().run()
