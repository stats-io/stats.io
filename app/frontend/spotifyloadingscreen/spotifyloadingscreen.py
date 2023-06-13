from kivymd.uix.screen import MDScreen
from app.backend.spotify.data_updater import SpotifyProcessData
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.config import Config

Config.set('kivy', 'exit_on_escape', '0')


class SpotifyLoadingScreen(MDScreen):
    sp = None
    _counter = 0

    def start_processing(self, file_path):
        self.start_animation()
        process = SpotifyProcessData(file_path)
        process.process_data_from_file()
        process.process_data_from_spotipy(self.sp)
        self.manager.get_screen("spotifyuserscreen").generate_screens()

    def _update_label(self, *args):
        if self._counter < 100:
            self._counter += 1
            self.manager.get_screen(
                "spotifyloadingscreen"
            ).ids.loadinglabel.text = f"{self._counter}%"
        else:
            self.__timer.cancel()
            self.manager.current = "spotifyuserscreen"

    def _animation(self, *args):
        self.__timer = Clock.schedule_interval(self._update_label, 0.01)

    def start_animation(self):
        self._counter = 0
        self.__timer = Clock
        self.__timer.schedule_once(self._animation, 0)

    def skip_processing(self):
        process = SpotifyProcessData()
        process.process_data_from_spotipy(self.sp)
        self.manager.get_screen("spotifyuserscreen").generate_screens()
        self.manager.current = "spotifyuserscreen"

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *args):
        if key == 27:
            x = MDApp()
            x.stop()
