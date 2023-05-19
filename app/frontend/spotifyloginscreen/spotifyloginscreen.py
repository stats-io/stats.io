from kivymd.uix.screen import MDScreen


class SpotifyLoginScreen(MDScreen):
    def skip_login(self):
        self.parent.current = "spotifyuserscreen"
