from kivymd.uix.screen import MDScreen


class SpotifyNewDataScreen(MDScreen):
    def skip_processing_data(self):
        self.parent.current = "spotifyloginscreen"
