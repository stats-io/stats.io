from time import sleep
from threading import Thread

from kivy.clock import Clock
from kivymd.uix.screen import MDScreen

import app.backend.netflixloading as Loading


class NetflixLoadingScreen(MDScreen):

    def _update_label(self, *args):
        if self.__counter < self.__num and self.__loading_screen.finishedLoading == 0:
            self.__counter += 1
            percent = self.__counter * 100 // self.__num
            self.manager.get_screen("netflixloadingscreen").ids.loadinglabel.text = f"{percent}%"
        else:
            self.manager.get_screen("netflixloadingscreen").ids.loadinglabel.text = f"100%"
            while not self.__loading_screen.finishedLoading:
                sleep(1)
            self.__timer.cancel()
            self.skip_processing()

    def _animation_handler(self, *args):
        self.__loading_screen = Loading.NetflixLoadingScreen()
        est_time, self.__num = self.__loading_screen.get_estimated_time(self.__file_path)
        backend_thread = Thread(target=self.__loading_screen.start_processing_data).start()
        self.manager.get_screen("netflixloadingscreen").ids.estimatedtime.text = f"Estimated time: {round(self.__num * est_time)}s"
        self.__timer = Clock.schedule_interval(self._update_label, est_time)

    def start_processing(self, file_path):
        self.__counter = 0
        self.__file_path = file_path
        self.__timer = Clock
        self.__timer.schedule_once(self._animation_handler, 0)

    def skip_processing(self):
        self.manager.get_screen("netflixuserscreen").generate_screens()
        self.manager.current = "netflixuserscreen"
