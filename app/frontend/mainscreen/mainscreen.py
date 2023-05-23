from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "fb34b1a1fb884d5794990d691867df0f"
CLIENT_SECRET = "185c998c2b0449378b992a237cc418ea"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-read-recently-played user-top-read"


class MainScreen(MDScreen):
    def login_screen(self):
        if os.path.isfile(".cache"):
            sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    redirect_uri=REDIRECT_URI,
                    scope=SCOPE,
                )
            )
            self.parent.get_screen("spotifyloadingscreen").sp = sp
            self.parent.current = "spotifynewdatascreen"
        else:
            self.parent.current = "spotifyloginscreen"

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *largs):
        if key == 27:
            x = MDApp()
            x.stop()

