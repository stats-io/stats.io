import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class NetflixCharts:

    def __init__(self,file = './Final_Data.csv'):
        self.csvFile = file

    def VisualizeCharts(self):
        self.DatesChart()
        self.SeriesvsFilmChart()

    def DatesChart(self):
        self.DataArray = pd.read_csv(self.csvFile)
        dates_counter = {}
        for ind, row in self.DataArray.iterrows():
            dates = row['Dates']
            dates = eval(dates)
            for dates1 in dates:
                if type(dates1) != list:
                    dates_counter[dates1] = dates_counter.get(dates1, 0) + 1
                else:
                    for date in dates1:
                        dates_counter[date] = dates_counter.get(date, 0) + 1
        Dates = pd.DataFrame.from_dict(dates_counter, orient='index', columns=['value'])
        Dates = Dates.sort_values('value', ascending=False)
        y = Dates.index
        tmp = pd.DataFrame(columns=['date'])
        for i, date in enumerate(y):
            date_obj = datetime.strptime(date, '%m/%d/%y')
            tmp.loc[i] = date_obj.strftime('%d-%m-%Y')
        tmp['date'] = pd.to_datetime(tmp['date'], format='%d-%m-%Y')
        Dates.index = tmp['date']
        Dates = Dates.sort_values('date')
        y = Dates.index
        tmp = pd.DataFrame(columns=['date'])
        for i, date in enumerate(y):
            data = str(date)
            tmp.loc[i] = data[0:-12]
        Dates.index = tmp['date']
        Dates = Dates.groupby(Dates.index).sum()

        fig, ax = plt.subplots(figsize=(10, 5))
        Dates.plot(kind='bar', ax=ax)
        ax.set_title('Wykres wartości w czasie')
        ax.set_xlabel('Data')
        ax.set_ylabel('Wartość')
        plt.xticks(fontsize=6.5)
        plt.xticks(rotation=90)
        plt.show()

    def SeriesvsFilmChart(self):
        film_counter = len(self.DataArray[self.DataArray['type'] == 'film'])
        series_counter = len(self.DataArray[self.DataArray['type'] == 'series'])
        sizes = [film_counter, series_counter]
        colors = ['#006400', '#008000']  # ciemnozielony, zielony
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, colors=colors, labels=['films', 'series'], autopct='%1.1f%%', startangle=90)
        ax1.set_title('Proporcje filmów i seriali')
        plt.show()
