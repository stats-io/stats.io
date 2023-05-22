from kivymd.uix.screen import MDScreen
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import (
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
)


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
