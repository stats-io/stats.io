from kivymd.uix.screen import MDScreen


class SpotifyNewDataScreen(MDScreen):
    def start_processing_data(self):
        self.parent.get_screen("spotifyloadingscreen").start_processing()
        self.parent.current = "spotifyloadingscreen"

    def skip_processing_data(self):
        self.parent.get_screen("spotifyloadingscreen").skip_processing()
        self.parent.current = "spotifyuserscreen"
