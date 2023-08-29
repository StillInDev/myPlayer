import os

import pygame
import sounddevice
import soundfile
import time


import numpy as np
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button










from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

from myPlayer.myPlayer.scripts.songs import Song
from myPlayer.myPlayer.scripts.library import LibraryScreen

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

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty

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


class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        self.start_time = None
        self.playing = False
        self.played = False
        self.playback_data = None
        self.playback_position = 0

        self.dex = 0
        self.song_list = song_list
        self.reload = True
        self.progress = 0.0
        self.song_length_seconds = 0.0
        self.prog_ev = None  # Initialize the clock event reference
        self.dragging = False

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
       
        
    def on_progress_touch_down(self, touch):
        self.dragging = True
        self.update_progress_from_touch(touch)

    def on_progress_touch_move(self, touch):
        if self.dragging:
            self.update_progress_from_touch(touch)

    def on_progress_touch_up(self, touch):
        if self.dragging:
            self.update_progress_from_touch(touch)
            self.dragging = False

    def update_progress_from_touch(self, touch):
        if self.progress_bar.collide_point(*touch.pos):
            touch_x = touch.pos[0] - self.progress_bar.x
            normalized_progress = touch_x / self.progress_bar.width
            self.progress = normalized_progress * self.song_length_seconds
            self.progress_bar.value = self.progress
            pygame.mixer.music.set_pos(self.progress)

    def load_song(self):
        print("Loading song:", song_list[index])
        pygame.mixer.init()
        pygame.mixer.music.load(self.song_list[self.dex].path)


        # Load audio data for precise playback control
        try:
            self.playback_data, _ = soundfile.read(self.song_list[self.dex].path, dtype='int16')
        except Exception as e:
            print("Error loading audio:", e)

    def find_song(self, title):
        i = [idx for idx, instance in enumerate(song_list) if title in instance.path]
        return i

    
    def play_song(self, select=None):
        if select is not None:
            # Find the song with text
            self.dex = self.find_song(select)[0]

        print('start', self.start_time)
        if not self.playing:
            self.playing = True
            self.ids.play_button.text = 'Pause'
            self.ids.play_button.background_color = 1, 0, 0, 1  # Red for pause state


            if self.playback_data is None or self.reload:
                self.reload = False
                self.load_song()

            self.start_time = time.time() - self.playback_position / SAMPLE_RATE
            sounddevice.play(self.playback_data[self.playback_position:], SAMPLE_RATE)

            pygame.mixer.init()
            pygame.mixer.music.load(song_list[index])

            # Get song length in seconds and store it as an attribute
            self.song_length_seconds = pygame.mixer.Sound(song_list[index]).get_length()
            print("Song Length:", self.song_length_seconds, "seconds")

            # Remove the old progress_bar if present
            if hasattr(self, 'progress_bar'):
                self.ids.progress_layout.remove_widget(self.progress_bar)
            
            # Add the new progress_bar to the layout
            self.progress_bar = ProgressBar(max=self.song_length_seconds, value=0)
            self.ids.progress_layout.add_widget(self.progress_bar)

            pygame.mixer.music.play()
            self.prog_ev = Clock.schedule_interval(self.update_progress, 1.0)


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

    def update_progress(self, dt):
        if self.playing:  # Only update progress if music is playing
            if self.progress < self.song_length_seconds:
                self.progress += 1  # Update value.
                self.progress_bar.value = self.progress  # Update progress bar value
                print("incremented")
                print(self.progress)
            else:
                self.progress = 0  # Reset value.
                print("reset")
                if self.prog_ev:
                    self.prog_ev.cancel()  # Stop updating.

    # Rest of the code...



    def skip_song(self):
        global index
        # pygame.mixer.music.stop()

        # Increment the index to skip to the next song
        index = (index + 1) % len(song_list)  # Loop back to the first song if needed

        # Load and play the new song
        self.progress = 0.0  # Reset value.
        self.load_song()
        self.play_song()
    



# Main class
class MyApp(App):
    # Starts loading the application

    def build(self):
        build_song_list(self)
        print(song_list)

        self.playMusicScreen = PlayScreen(name='playMusicScreen')
        self.libraryScreen = LibraryScreen(name='library', song_list=song_list)

        # Loads screen
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))

        sm.add_widget(self.playMusicScreen)
        sm.add_widget(self.libraryScreen)




        sm.add_widget(PlayScreen(name='play'))
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
