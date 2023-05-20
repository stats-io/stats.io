from kivymd.uix.screen import MDScreen
from app.backend.spotifyproccesdata import SpotifyProcessData
from kivy.clock import Clock


class SpotifyLoadingScreen(MDScreen):
    sp = None
    _counter = 0

    def start_processing(self):
        process = SpotifyProcessData()
        process.process_data_from_spotipy(self.sp)
        self.skip_processing()

    def _update_label(self, *args):
        if self._counter < 100:
            self._counter += 1
            self.manager.get_screen(
                "spotifyloadingscreen"
            ).ids.loadinglabel.text = f"{self._counter}%"
        else:
            self.__timer.cancel()
            self.skip_processing()
            self.manager.current = "spotifyuserscreen"

    def _animation(self, *args):
        self.__timer = Clock.schedule_interval(self._update_label, 0.1)

    def start_animation(self):
        self._counter = 0
        self.__timer = Clock
        self.__timer.schedule_once(self._animation, 0)

    def skip_processing(self):
        self.manager.get_screen("spotifyuserscreen").generate_screens()
        self.manager.current = "spotifyuserscreen"
