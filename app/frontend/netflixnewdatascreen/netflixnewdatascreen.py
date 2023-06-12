import os
import pandas as pd
from kivy.core.window import Window
from kivy.config import Config

Config.set('kivy', 'exit_on_escape', '0')
from kivy import platform
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from plyer import filechooser
import shutil

user_file = os.path.abspath("app/backend/netflix/database/last_upload.csv")
last_data = os.path.abspath("app/backend/netflix/database/last_file.csv")


class NetflixNewDataScreen(MDScreen):
    __banner_open = False
    dialog = None
    button_press = 0
    private_files = []

    def help_banner_handler(self):
        if not self.__banner_open:
            self.parent.get_screen("netflixnewdatascreen").ids.banner.show()
            self.parent.get_screen(
                "netflixnewdatascreen"
            ).ids.bannericon.icon = "chevron-up"
        else:
            self.parent.get_screen("netflixnewdatascreen").ids.banner.hide()
            self.parent.get_screen(
                "netflixnewdatascreen"
            ).ids.bannericon.icon = "chevron-down"
        self.__banner_open = not self.__banner_open

    def start_processing_data(self):
        try:
            if platform == "android":
                from jnius import autoclass

                version = autoclass("android.os.Build$VERSION")
                android_version = version.RELEASE
                if int(android_version) >= 10:
                    shutil.copy(self.private_files[0], user_file)
                    self.parent.get_screen("netflixloadingscreen").start_processing(
                        self.private_files[0]
                    )
                else:
                    shutil.copy(self.destination_path, user_file)
                    self.parent.get_screen("netflixloadingscreen").start_processing(
                        self.destination_path
                    )
            else:
                shutil.copy(self.destination_path, user_file)
                self.parent.get_screen("netflixloadingscreen").start_processing(
                    self.destination_path
                )
            self.parent.current = "netflixloadingscreen"
        except pd.errors.EmptyDataError:
            self.dialog = MDDialog(
                text="Please, add a file to enjoy your data!",
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

    def skip_processing_data(self):
        try:
            df = pd.read_csv(last_data)
            self.parent.get_screen("netflixloadingscreen").skip_processing()
            self.parent.current = "netflixuserscreen"
        except pd.errors.EmptyDataError:
            self.dialog = MDDialog(
                text="""This is your first time using of this app, 
follow the instructions above and add a csv file!""",
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

    def file_manager_open(self):
        if platform == "android":
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

    def WrongFile(self):
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

    def __handle_selection(self, selection):
        if selection:
            file_path = selection[0]
            try:
                df = pd.read_csv(file_path)
                required_columns_1 = ["Title", "Date"]
                required_columns_2 = [
                    "Profile Name",
                    "Start Time",
                    "Duration",
                    "Attributes",
                    "Title",
                    "Supplemental Video Type",
                    "Device Type",
                    "Bookmark",
                    "Latest Bookmark",
                    "Country",
                ]
                if all(column in df.columns for column in required_columns_1) or all(
                    column in df.columns for column in required_columns_2
                ):
                    self.parent.get_screen(
                        "netflixnewdatascreen"
                    ).ids.filemanagericon.icon = "check-circle"
                    self.parent.get_screen(
                        "netflixnewdatascreen"
                    ).ids.fileadd.text = "Chosen file"
                    self.parent.get_screen(
                        "netflixnewdatascreen"
                    ).ids.filename.text = f"{file_path}"
                    self.destination_path = file_path
                    df.to_csv(self.destination_path, index=False)
                else:
                    self.WrongFile()
            except Exception:
                self.WrongFile()

        else:
            pass

    def chooser_callback(self, shared_file_list):
        from androidstorage4kivy import SharedStorage

        ss = SharedStorage()
        for shared_file in shared_file_list:
            self.private_files.append(ss.copy_from_shared(shared_file))

        if self.private_files:
            path = self.private_files[0]
            self.parent.get_screen(
                "netflixnewdatascreen"
            ).ids.filemanagericon.icon = "check-circle"
            self.parent.get_screen(
                "netflixnewdatascreen"
            ).ids.fileadd.text = "Chosen file"
            self.parent.get_screen("netflixnewdatascreen").ids.filename.text = f"{path}"

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *largs):
        if key == 27:
            self.parent.current = "mainscreen"
