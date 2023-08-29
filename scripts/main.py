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


class TrimPopup(Popup):
    start_time = StringProperty()
    end_time = StringProperty()

    def __init__(self, song_path, **kwargs):
        super(TrimPopup, self).__init__(**kwargs)
        self.song_path = song_path

    def trim_song(self):
        try:
            start_time = int(self.start_time) * 1000  # Convert to milliseconds
            end_time = int(self.end_time) * 1000  # Convert to milliseconds

            parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            song_path = os.path.join(parent_directory, 'songs', self.song_path)  # Full path to the song

            song = AudioSegment.from_mp3(song_path)  # Load the audio segment from the song file
            trimmed_song = song[start_time:end_time]

            # Prompt the user for a new filename
            new_filename = input("Enter a new filename for the trimmed song (without extension): ")
            if not new_filename:
                print("Invalid filename. The song will be saved with a default name.")
                new_filename = "trimmed_song"

            trimmed_filename = f"{new_filename}.mp3"
            trimmed_song_path = os.path.join(parent_directory, 'trimmedsongs', trimmed_filename)

            trimmed_song.export(trimmed_song_path, format="mp3")
            print(f"Song trimmed and saved as '{trimmed_filename}' in the 'trimmedsongs' folder")
        except Exception as e:
            print("Error trimming song:", e)


class QuietPopup(Popup):
    start_time = StringProperty()
    end_time = StringProperty()

    def __init__(self, song_path, **kwargs):
        super(QuietPopup, self).__init__(**kwargs)
        self.song_path = song_path

    def quiet_song(self):
        try:
            start_time = int(self.start_time) * 1000  # Convert to milliseconds
            end_time = int(self.end_time) * 1000  # Convert to milliseconds

            parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            song_path = os.path.join(parent_directory, 'songs', self.song_path)  # Full path to the song

            song = AudioSegment.from_mp3(song_path)  # Load the audio segment from the song file

            # Apply the quiet effect to the specified time range
            silence = AudioSegment.silent(duration=end_time - start_time)
            quiet_part = song[:start_time] + silence + song[end_time:]

            # Create a new filename for the modified song
            new_filename = f"quiet_{os.path.basename(self.song_path)}"
            quiet_song_path = os.path.join(parent_directory, 'quietsongs', new_filename)

            # Export the modified song
            quiet_part.export(quiet_song_path, format="mp3")
            print(f"Song with quiet effect applied saved as '{new_filename}' in the 'quietsongs' folder")
        except Exception as e:
            print("Error applying quiet effect:", e)


class TrimScreen(Screen):
    def __init__(self, **kwargs):
        super(TrimScreen, self).__init__(**kwargs)
        self.song_buttons = []  # List to hold Button widgets

    def on_pre_enter(self, *args):
        self.populate_song_list()

    def populate_song_list(self):
        song_list_layout = BoxLayout(orientation='vertical')

        for song_path in song_list:
            song_button = Button(text=os.path.basename(song_path), on_release=self.select_song)
            self.song_buttons.append(song_button)
            song_list_layout.add_widget(song_button)

        scroll_view = ScrollView()
        scroll_view.add_widget(song_list_layout)
        self.ids.song_list_container.add_widget(scroll_view)

    def select_song(self, button):
        selected_song = button.text
        print("Selected song:", selected_song)
        trim_popup = TrimPopup(title="Trim Song", song_path=selected_song)
        trim_popup.open()


class EditScreen(Screen):
    def trim_song(self):
        pass


class QuietScreen(Screen):
    def on_pre_enter(self, *args):
        self.populate_song_list()

    def populate_song_list(self):
        song_list_layout = BoxLayout(orientation='vertical')

        for song_path in song_list:
            song_button = Button(text=os.path.basename(song_path), on_release=self.open_quiet_popup)
            song_list_layout.add_widget(song_button)

        scroll_view = ScrollView()
        scroll_view.add_widget(song_list_layout)
        self.ids.song_list_container.add_widget(scroll_view)

    def open_quiet_popup(self, button):
        selected_song = button.text
        print("Selected song:", selected_song)
        quiet_popup = QuietPopup(title="Apply Quiet Effect", song_path=selected_song)
        quiet_popup.open()


class SpeedScreen(Screen):
    pass


class SlowScreen(Screen):
    pass


class SettingsScreen(Screen):
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
