from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.config import Config

Config.set('kivy', 'exit_on_escape', '0')

class SpotifyNewDataScreen(MDScreen):
    def start_processing_data(self):
        self.parent.get_screen("spotifyloadingscreen").start_processing()
        self.parent.current = "spotifyloadingscreen"

    def skip_processing_data(self):
        self.parent.get_screen("spotifyloadingscreen").skip_processing()
        self.parent.current = "spotifyuserscreen"

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *largs):
        if key == 27:
            self.parent.current = "mainscreen"
