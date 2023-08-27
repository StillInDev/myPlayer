import os
import pygame
import sounddevice
import soundfile
import time
import numpy as np

from pydub import AudioSegment
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# Holds all songs
song_list = []

index = 0

'''#---------------SCREENS---------------#'''


class MenuScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class PlayScreen(Screen):
    # SO WE NEED TO KEEP TRACK OF WHERE YOU LEFT OFF IN LAST PLAYLIST
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        self.start_time = None
        self.playing = False  # Track play/pause state
        self.played = False
        # self.curr_song = AudioSegment.from_file(song_list[index])
        self.playback_data = None
        self.playback_position = 0

    def load_song(self):
        pygame.mixer.init()
        pygame.mixer.music.load(song_list[index])

        # Load audio data for precise playback control
        self.playback_data, _ = soundfile.read(song_list[index], dtype='int16')

    # def play_song(self):
        # if not self.playing:
        #     self.playing = True
        #     self.ids.play_button.text = 'Pause'
        #     self.ids.play_button.background_color = 1, 0, 0, 1  # Red for pause state
        #
        #     if not self.playback_data is None:
        #         self.load_song()
        #
        #     self.start_time = time.time()
        #     sounddevice.play(self.playback_data[self.playback_position:], 44100)
        # else:
        #     self.playing = False
        #     self.ids.play_button.text = 'Play'
        #     self.ids.play_button.background_color = 0, 1, 0, 1  # Green for play state
        #
        #     elapsed_time = time.time() - self.start_time
        #     self.playback_position += int(elapsed_time * 44100)  # Convert to samples
        #     sounddevice.stop()

    def play_song(self):

        if not self.playing:
            # MIGHT HAVE AN ISSUE WITH A CHANGE IN SONG
            self.playing = True
            self.ids.play_button.text = 'Pause'
            self.ids.play_button.background_color = 1, 0, 0, 1  # Red for pause state

            pygame.mixer.init()
            pygame.mixer.music.load(song_list[index])
            pygame.mixer.music.play()
        else:
            self.playing = False
            self.ids.play_button.text = 'Play'
            self.ids.play_button.background_color = 0, 1, 0, 1  # Green for play state

            pygame.mixer.music.stop()


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

        return sm

        # Wait for the song to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


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
