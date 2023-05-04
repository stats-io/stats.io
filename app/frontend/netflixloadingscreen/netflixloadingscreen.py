from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


class NetflixLoadingScreen(MDScreen):
    _counter = 0

    def _update_label(self, *args):
        if self._counter < 100:
            self._counter += 1
            self.manager.get_screen("netflixloadingscreen").ids.loadinglabel.text = f"{self._counter}%"
        else:
            self.manager.current = "netflixuserscreen"

    def _animation(self, *args):
        Clock.schedule_interval(self._update_label, 0.1)

    def start_animation(self):
        self._counter = 0
        Clock.schedule_once(self._animation, 0)
