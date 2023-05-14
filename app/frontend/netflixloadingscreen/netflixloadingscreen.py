from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


class NetflixLoadingScreen(MDScreen):
    _counter = 0

    def _update_label(self, *args):
        if self._counter < 100:
            self._counter += 1
            self.manager.get_screen("netflixloadingscreen").ids.loadinglabel.text = f"{self._counter}%"
        else:
            self.clock_variable.cancel()
            self.manager.current = "netflixuserscreen"
            self.manager.get_screen("netflixuserscreen").generate_charts()

    def _animation(self, *args):
        self.clock_variable = Clock.schedule_interval(self._update_label, 0.001)

    def start_animation(self):
        self._counter = 0
        Clock.schedule_once(self._animation, 0)

    def skip_animation(self):
        self.manager.get_screen("netflixuserscreen").generate_charts()
