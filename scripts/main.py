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

from myPlayer.myPlayer.scripts.playscreen import PlayScreen
from myPlayer.myPlayer.scripts.songs import Song
from myPlayer.myPlayer.scripts.library import LibraryScreen

from kivy.lang import Builder

# Combines all the .kv files specified
Builder.load_file('menuScreen.kv')
Builder.load_file('settingScreen.kv')
Builder.load_file('playScreen.kv')

# Holds all songs
song_list = []
library_pages = []

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
        build_song_list(self)
        print(song_list)

        self.playMusicScreen = PlayScreen(name='playMusicScreen', song_list=song_list, sample_rate=SAMPLE_RATE)
        self.libraryScreen = LibraryScreen(name='library', song_list=song_list)

        # Loads screen
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(self.playMusicScreen)
        sm.add_widget(self.libraryScreen)
        sm.add_widget(EditScreen(name='edit'))
        sm.add_widget(TrimScreen(name='trim'))
        sm.add_widget(QuietScreen(name='quiet'))
        sm.add_widget(SlowScreen(name='slow'))
        sm.add_widget(SpeedScreen(name='speed'))

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
