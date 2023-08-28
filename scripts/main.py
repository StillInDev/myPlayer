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








from pydub import AudioSegment
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# Holds all songs
song_list = []

index = 0

'''#---------------SCREENS---------------#'''


class MenuScreen(Screen):
    pass

class EditScreen(Screen):
    def trim_song(self):
        pass

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
        # Perform further actions with the selected song




class QuietScreen(Screen):
    pass
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
        self.progress = 0.0
        self.song_length_seconds = 0.0
        self.prog_ev = None  # Initialize the clock event reference
        self.dragging = False
        
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
        pygame.mixer.music.load(song_list[index])

        try:
            self.playback_data, _ = soundfile.read(song_list[index], dtype='int16')
        except Exception as e:
            print("Error loading audio:", e)

    def play_song(self):
        if not self.playing:
            self.playing = True
            self.ids.play_button.text = 'Pause'
            self.ids.play_button.background_color = 1, 0, 0, 1  # Red for pause state

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

            pygame.mixer.music.stop()

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

        # Loads screen
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(PlayScreen(name='play'))
        sm.add_widget(EditScreen(name='edit'))
        sm.add_widget(TrimScreen(name='trim'))
        sm.add_widget(QuietScreen(name='quiet'))
        sm.add_widget(SlowScreen(name='slow'))
        sm.add_widget(SpeedScreen(name='speed'))
        




        return sm

        # # Wait for the song to finish playing
        # while pygame.mixer.music.get_busy():
        #     pygame.time.Clock().tick(10)


def build_song_list(self):
    # Get song folder path
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    song_folder_path = os.path.join(parent_directory, 'songs')

    # Fill song_list with all songs
    for filename in os.listdir(song_folder_path):
        if filename.endswith('.mp3'):
            song_path = os.path.join(song_folder_path, filename)
            song_list.append(song_path)
            # self.song_list.append(os.path.join(song_folder_path, filename))    ->     This adds the path


if __name__ == '__main__':
    MyApp().run()
