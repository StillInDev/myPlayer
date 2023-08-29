import os

import pygame
import sounddevice
import soundfile
import time

from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen


class PlayScreen(Screen):
    def __init__(self, song_list, sample_rate, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        self.start_time = None
        self.playing = False
        self.played = False
        self.playback_data = None
        self.playback_position = 0

        self.sample_rate = sample_rate
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

        self.progress = 0.0
        self.load_song()
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
        print("Loading song:", self.song_list[self.dex])
        pygame.mixer.init()
        pygame.mixer.music.load(self.song_list[self.dex].path)

        # Load audio data for precise playback control
        try:
            self.playback_data, _ = soundfile.read(self.song_list[self.dex].path, dtype='int16')
        except Exception as e:
            print("Error loading audio:", e)

    def find_song(self, title):
        i = [idx for idx, instance in enumerate(self.song_list) if title in instance.path]
        return i[0]

    def play_song(self, select=None):
        if select is not None:
            # Find the song with text
            self.dex = self.find_song(select)

        print('start', self.start_time)
        if not self.playing:
            self.playing = True
            self.ids.play_button.text = 'Pause'
            self.ids.play_button.background_color = 1, 0, 0, 1  # Red for pause state

            if self.playback_data is None or self.reload:
                self.reload = False
                self.load_song()

            self.start_time = time.time() - self.playback_position / self.sample_rate
            sounddevice.play(self.playback_data[self.playback_position:], self.sample_rate)

            pygame.mixer.init()
            pygame.mixer.music.load(self.song_list[self.dex].path)

            # Get song length in seconds and store it as an attribute
            self.song_length_seconds = pygame.mixer.Sound(self.song_list[self.dex].path).get_length()
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
            self.playback_position += int(elapsed_time * self.sample_rate)  # Convert to samples
            sounddevice.stop()

    def update_time(self):
        if self.playing:
            elapsed_time = time.time() - self.start_time
            self.playback_position += int(elapsed_time * self.sample_rate)  # Convert to samples
            self.start_time = time.time()

    def on_playback_position(self, dt):
        self.update_time()
        if self.playing:
            print("Elapsed Time:", self.playback_position / self.sample_rate)

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
