import math
import time

from kivy.clock import Clock
import threading
from kivymd.uix.screen import MDScreen
import app.backend.NetflixLoadingScreen as LS


class NetflixLoadingScreen(MDScreen):
    _counter = 0

    def _update_label(self, *args):
        if self._counter < self.num and self.X.finishedLoading == 0:
            self._counter += 1
            self.manager.get_screen("netflixloadingscreen").ids.loadinglabel.text = f"{self._counter}/{self.num}"
        else:
            # Poprawic zeby zapelnialo 100/100
            self.manager.get_screen("netflixloadingscreen").ids.loadinglabel.text = f"{self.num}/{self.num}"
            while True:
                time.sleep(1)
                if (self.X.finishedLoading == 1): break
            self.Zegar.cancel()
            self.manager.get_screen("netflixuserscreen").generate_charts()
            self.manager.current = "netflixuserscreen"

    def _animation(self, *args):
        self.X = LS.NetflixLoadingScreen()
        self.time, self.num = self.X.Time()
        self.num = math.ceil(self.num * 1.5)
        self.manager.get_screen("netflixloadingscreen").ids.estimatedtime.text = f"Estimated Time {round((self.num * self.time),2)}s"
        watek2 = threading.Thread(target=self.X.StartUpdatingData)
        watek2.start()
        self.Zegar = Clock.schedule_interval(self._update_label, self.time)

    def start_animation(self):
        self.Zegar = Clock
        self.Zegar.schedule_once(self._animation, 0)

    def skip_animation(self):
        self.manager.get_screen("netflixuserscreen").generate_charts()
