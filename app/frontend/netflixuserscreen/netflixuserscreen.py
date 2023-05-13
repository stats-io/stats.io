from kivymd.uix.screen import MDScreen
from kivymd.uix.list import ThreeLineListItem
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from app.backend.NetflixCharts import NetflixCharts
from app.backend.NetflixMainScreen import NetflixMainScreen
import pandas as pd


class CustomThreeLineListItem(ThreeLineListItem):
    pass


class NetflixUserScreen(MDScreen):
    netflix_main_screen = NetflixMainScreen()
    charts = NetflixCharts()

    def generate_charts(self):
        creator = self.manager.get_screen("netflixuserscreen").ids.box
        creator.add_widget(FigureCanvasKivyAgg(self.charts.GenresChart()))
        creator = self.manager.get_screen("netflixuserscreen").ids.boxik
        creator.add_widget(FigureCanvasKivyAgg(self.charts.SeriesvsFilmChart()))
        creator = self.manager.get_screen("netflixuserscreen").ids.boxer
        creator.add_widget(FigureCanvasKivyAgg(self.charts.DatesChart()))
        creator = self.manager.get_screen("netflixuserscreen").ids.boks
        creator.add_widget(FigureCanvasKivyAgg(self.charts.Favourite_year()))
        self.generate_history()


    def generate_history(self):
        with open('app/backend/BigFile.csv', 'r') as file:
            df = pd.read_csv(file)
            data_array = df.to_dict('records')
            self.create_list(data_array)


    def create_list(self, data_array):
        lista = self.manager.get_screen("netflixuserscreen").ids.netflixhistoryscreen
        for row in range(len(data_array)):
            third = ', '.join(list(set(data_array[row]['Dates'].replace('[', '').replace(']', '').replace('\'', '').split(', '))))
            lista.add_widget(
                CustomThreeLineListItem(
                    text = data_array[row]['title'],
                    secondary_text = data_array[row]['genres'].replace('[', '').replace(']', '').replace('\'', ''),
                    tertiary_text = third,
                )
            )