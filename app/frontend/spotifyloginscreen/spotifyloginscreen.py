from kivymd.uix.screen import MDScreen
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from kivy.core.window import Window
from kivy.config import Config

Config.set('kivy', 'exit_on_escape', '0')

CLIENT_ID = "fb34b1a1fb884d5794990d691867df0f"
CLIENT_SECRET = "-"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-read-recently-played user-top-read"


class SpotifyLoginScreen(MDScreen):
    def login(self):
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=REDIRECT_URI,
                scope=SCOPE,
            )
        )
        user = sp.current_user()
        self.parent.get_screen("spotifyloadingscreen").sp = sp
        self.parent.current = "spotifynewdatascreen"

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *largs):
        if key == 27:
            self.parent.current = "mainscreen"
