import math
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
            self.manager.get_screen("netflixloadingscreen").ids.loadinglabel.text = f"{self.num}/{self.num}"
            while True:

                if (self.X.finishedLoading == 1): break
            self.manager.current = "netflixuserscreen"
            self.manager.get_screen("netflixuserscreen").generate_charts()

    def _animation(self, *args):
        self.X = LS.NetflixLoadingScreen()
        self.time, self.num = self.X.Time()
        self.num = math.ceil(self.num * 1.5)
        self.manager.get_screen("netflixloadingscreen").ids.estimatedtime.text = f"Estimated Time {round((self.num * self.time),2)}s"
        watek1 = threading.Thread(target=self._update_label)
        watek2 = threading.Thread(target=self.X.StartUpdatingData)
        watek1.start()
        watek2.start()
        Clock.schedule_interval(self._update_label, self.time)


    def start_animation(self):
        Clock.schedule_once(self._animation, 0)

    def skip_animation(self):
        self.manager.get_screen("netflixuserscreen").generate_charts()
