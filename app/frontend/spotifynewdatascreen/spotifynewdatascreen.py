from kivymd.uix.screen import MDScreen


class SpotifyNewDataScreen(MDScreen):
    def start_processing_data(self):
        self.parent.get_screen("spotifyloadingscreen").start_processing()
        self.parent.current = "spotifyloadingscreen"
        self.parent.get_screen("spotifyloadingscreen").start_animation()

    def skip_processing_data(self):
        self.parent.get_screen("spotifyloadingscreen").start_processing()
        self.parent.current = "spotifyuserscreen"
