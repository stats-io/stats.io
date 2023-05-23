from kivymd.uix.screen import MDScreen
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "fb34b1a1fb884d5794990d691867df0f"
CLIENT_SECRET = "185c998c2b0449378b992a237cc418ea"
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
