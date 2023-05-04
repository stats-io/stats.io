from kivymd.uix.screen import MDScreen


class NetflixNewDataScreen(MDScreen):
    _banner_handler = True

    def help_banner_handler(self):
        if self._banner_handler == True:
            self._show_banner()
        else:
            self._hide_banner()
        self._banner_handler = not self._banner_handler

    def start_processing_data(self):
        self.parent.get_screen("netflixloadingscreen").start_animation()
        self.parent.current = "netflixloadingscreen"

    def _show_banner(self):
        self.parent.get_screen("netflixnewdatascreen").ids.banner.show()
        self.parent.get_screen("netflixnewdatascreen").ids.bannericon.icon = "chevron-up"

    def _hide_banner(self):
        self.parent.get_screen("netflixnewdatascreen").ids.banner.hide()
        self.parent.get_screen("netflixnewdatascreen").ids.bannericon.icon = "chevron-down"
