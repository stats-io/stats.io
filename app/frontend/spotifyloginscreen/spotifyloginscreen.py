from kivymd.uix.screen import MDScreen
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE
from kivy.core.window import Window
from kivy.config import Config

Config.set('kivy', 'exit_on_escape', '0')


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
