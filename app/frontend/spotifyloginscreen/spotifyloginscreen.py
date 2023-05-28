from kivymd.uix.screen import MDScreen
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE


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
