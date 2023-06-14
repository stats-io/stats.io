from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.config import Config
from kivy import platform
from plyer import filechooser

Config.set('kivy', 'exit_on_escape', '0')


class SpotifyNewDataScreen(MDScreen):
    __banner_open = False
    dialog = None
    destination_path = None
    private_files = []

    def help_banner_handler(self):
        if not self.__banner_open:
            self.parent.get_screen("spotifynewdatascreen").ids.banner.show()
            self.parent.get_screen(
                "spotifynewdatascreen"
            ).ids.bannericon.icon = "chevron-up"
        else:
            self.parent.get_screen("spotifynewdatascreen").ids.banner.hide()
            self.parent.get_screen(
                "spotifynewdatascreen"
            ).ids.bannericon.icon = "chevron-down"
        self.__banner_open = not self.__banner_open

    def start_processing_data(self):
        if self.destination_path is not None:
            self.parent.get_screen("spotifyloadingscreen").start_processing(self.destination_path)
            self.parent.current = "spotifyloadingscreen"
            self.destination_path = None
        else:
            self.skip_processing_data()

    def skip_processing_data(self):
        self.parent.get_screen("spotifyloadingscreen").skip_processing()
        self.parent.current = "spotifyuserscreen"

    def file_manager_open(self):
        if platform == "android":
            self.private_files = []
            from jnius import autoclass

            version = autoclass("android.os.Build$VERSION")
            android_version = version.RELEASE
            if int(android_version) >= 10:
                from androidstorage4kivy import Chooser

                self.chooser = Chooser(self.chooser_callback)
                self.chooser.choose_content("*/*")
            else:
                filechooser.open_file(on_selection=self.__handle_selection)
        else:
            filechooser.open_file(on_selection=self.__handle_selection)

    def __handle_selection(self, selection):
        if selection:
            file_path = selection[0]
            if "my_spotify_data" in file_path:
                self.parent.get_screen(
                    "spotifynewdatascreen"
                ).ids.filemanagericon.icon = "check-circle"
                self.parent.get_screen(
                    "spotifynewdatascreen"
                ).ids.fileadd.text = "Chosen file"
                self.parent.get_screen(
                    "spotifynewdatascreen"
                ).ids.filename.text = f"{file_path}"
                self.destination_path = file_path
                self.file_added = True
            else:
                self.wrong_file_notification()
        else:
            pass

    def chooser_callback(self, shared_file_list):
        from androidstorage4kivy import SharedStorage

        ss = SharedStorage()
        for shared_file in shared_file_list:
            self.private_files.append(ss.copy_from_shared(shared_file))

        if self.private_files:
            path = self.private_files[0]
            if "my_spotify_data" in path:
                self.parent.get_screen(
                    "spotifynewdatascreen"
                ).ids.filemanagericon.icon = "check-circle"
                self.parent.get_screen(
                    "spotifynewdatascreen"
                ).ids.fileadd.text = "Chosen file"
                self.parent.get_screen("spotifynewdatascreen").ids.filename.text = f"{path}"
                self.destination_path = path
            else:
                self.wrong_file_notification()

    def wrong_file_notification(self):
        self.dialog = MDDialog(
            text="""You add a Wrong file!!!
Follow the instructions above""",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color="#080808",
                    on_release=self.close_dialog,
                ),
            ],
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *largs):
        if key == 27:
            self.parent.current = "mainscreen"
