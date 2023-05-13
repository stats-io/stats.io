import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class NetflixCharts:

    def __init__(self, file = ''):
        self.csvFile = 'app/backend/BigFile.csv'

    def VisualizeCharts(self):
        self.DatesChart()
        self.SeriesvsFilmChart()
        self.GenresChart()
        self.Favourite_year()
        DataArray = pd.read_csv(self.csvFile)
        if ~np.isnan(DataArray.iloc[0,6]):
            self.TimeAtSeries()

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
        isBig = 0
        for i, date in enumerate(y):
            try:
                date_obj = datetime.strptime(date, '%m/%d/%y')
                tmp.loc[i] = date_obj.strftime('%y-%m-%d')
            except ValueError:
                isBig = 1
                break
        if isBig == 0:
            tmp['date'] = pd.to_datetime(tmp['date'], format='%y-%m-%d')
            Dates.index = tmp['date']
        else:
            tmp['date'] = Dates.index
            Dates.index = tmp['date']

        Dates = Dates.sort_values('date')
        y = Dates.index
        tmp = pd.DataFrame(columns=['date'])
        for i, date in enumerate(y):
            data = str(date)
            if isBig == 0:
                tmp.loc[i] = data[0:-12]
            else:
                tmp.loc[i] = data[0:-3]
        Dates.index = tmp['date']
        Dates = Dates.groupby(Dates.index).sum()
        Dates.index = pd.to_datetime(Dates.index)
        Dates = Dates.resample('6M').sum()
        Dates.index = pd.to_datetime(Dates.index).strftime('%Y-%m')
        fig, ax = plt.subplots(figsize=(10, 5))
        Dates.plot(kind='bar', ax=ax, color='#A7F500', legend=False)
        ax.set_xticks(ax.get_xticks()[::2])
        ax.set_title('Wykres wartości w czasie')
        ax.set_xlabel('Data')
        ax.set_ylabel('Wartość')
        plt.xticks(fontsize=8)
        plt.xticks(rotation=90)
        ax.tick_params(colors='#E0E0E0')
        fig.patch.set_facecolor('#080808')
        ax.spines['bottom'].set_color('#A7F500')
        ax.spines['top'].set_color('#080808')
        ax.spines['right'].set_color('#080808')
        ax.spines['left'].set_color('#A7F500')
        ax.set_facecolor('#080808')
        return plt.gcf()

    def SeriesvsFilmChart(self):
        film_counter = len(self.DataArray[self.DataArray['type'] == 'film'])
        series_counter = len(self.DataArray[self.DataArray['type'] == 'series'])
        sizes = [film_counter, series_counter]
        colors = ['#A7F500', '#E0E0E0']
        fig, ax = plt.subplots()
        pie_wedge_collection, texts, autotexts = ax.pie(
            sizes, 
            colors=colors, 
            autopct='%1.1f%%', 
            startangle=90, 
            textprops={
                'color': '#080808', 
                'fontsize': 8, 
                'horizontalalignment': 'center', 
                'verticalalignment': 'center',
            }
        )
        labels = ['Films', 'Series']
        leg = ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), fontsize=8, ncol=2, edgecolor="#080808")
        fig.patch.set_facecolor('#080808')
        for text in leg.get_texts():
            text.set_color("#E0E0E0")
        leg._legend_title_box._text.set_color('#E0E0E0')
        leg.get_frame().set_facecolor('#080808')
        plt.subplots_adjust(bottom=0.5)
        return plt.gcf()


    def GenresChart(self):
        genres_counter = {}
        self.DataArray = pd.read_csv(self.csvFile)
        for ind, row in self.DataArray.iterrows():
            genres = row['genres']
            genres = eval(genres)
            for genre in genres:
                genres_counter[genre] = genres_counter.get(genre, 0) + 1
        Genres = pd.DataFrame.from_dict(genres_counter, orient='index', columns=['value'])
        Genres = Genres.sort_values('value', ascending=False)
        other_rows  = Genres[Genres['value'] <= 3]
        other_rows = other_rows['value'].sum()
        Genres = Genres[Genres['value'] > 3]
        other_row = pd.DataFrame({'value': [other_rows]}, index=['Others'])
        Genres = pd.concat([Genres, other_row])

        colors = ['#A7F500', '#C2F52B', '#DFF55C', '#F5F218', '#F5C118', '#F58B18', '#F55B18', '#F53518', '#F51818', '#E01B4F', '#E04F6F', '#E0828F', '#E0B5AF', '#E0E0CF', '#B5E0AF', '#82E082', '#4FE052', '#4FB56F', '#4FE0A3', '#4FE0CF', '#4FB5CF', '#4F82CF', '#4F4FCF', '#824FCF', '#B54FCF', '#E04FCF', '#E04F8F', '#E0B5CF', '#B5B5E0', '#8282E0', '#4F4FE0', '#666666']

        fig, ax = plt.subplots(facecolor='none')
        ax.pie(Genres['value'], labels=None, colors=colors)

        fig.patch.set_facecolor('#080808')
        ax.set_xlabel(None)
        leg = ax.legend(Genres.index, loc='upper center', bbox_to_anchor=(0.5, -0.1), fontsize=8, ncol=2, edgecolor="#080808")
        for text in leg.get_texts():
            text.set_color("#E0E0E0")
        leg._legend_title_box._text.set_color('#E0E0E0')
        leg.get_frame().set_facecolor('#080808')
        plt.subplots_adjust(bottom=0.5)
        return plt.gcf()

    def Favourite_year(self):
        Release_year = pd.read_csv(self.csvFile)
        Release_year['Release Date'] = Release_year['Release Date'].str.slice(0,4)
        Release_year = Release_year[['title','Release Date']]
        years_counter = {year: 0 for year in range(2000,2024)}
        for ind, row in Release_year.iterrows():
            year = row['Release Date']
            if type(year) is float: continue
            year = int(year)
            if year in years_counter.keys():
                years_counter[year] += 1
            else:
                years_counter[year] = 1
        sum_under_2000 = 0
        for key in list(years_counter.keys()):
            if key < 2000:
                sum_under_2000 += years_counter[key]
                years_counter.pop(key)
        years_counter[1999] = sum_under_2000
        Years = pd.DataFrame.from_dict(years_counter, orient='index', columns=['value'])
        Years = Years.sort_index(axis = 0)
        Years = Years.rename(index={1999: '<2000'})
        fig, ax = plt.subplots()
        Years.plot(kind='barh', ax=ax, color='#A7F500', legend=False)
        ax.set_yticks(ax.get_yticks()[-1::-2])
        ax.set_title('Lata z których obejrzano najwięcej tytułów')
        ax.set_xlabel('Data')
        ax.set_ylabel('Ilość obejrzanych filmów/seriali')

        ax.tick_params(colors='#E0E0E0')
        fig.patch.set_facecolor('#080808')
        ax.spines['bottom'].set_color('#A7F500')
        ax.spines['top'].set_color('#080808')
        ax.spines['right'].set_color('#080808')
        ax.spines['left'].set_color('#A7F500')
        ax.set_facecolor('#080808')

        return plt.gcf()

    def TimeAtSeries(self):
        DataArray = pd.read_csv('app/backend/BigFile.csv')
        DataArray = DataArray.sort_values('SumOfTime').tail(20)
        Result = DataArray[['title', 'SumOfTime']].copy()
        Result = Result[Result['SumOfTime'] >= 600]
        Result = Result.reset_index(drop=True)
        fig, ax = plt.subplots()


        ax.barh(Result['title'], Result['SumOfTime'] / 60, color="#A7F500", legend=False)
        ax.set_ylabel('Tytuły')
        ax.tick_params(axis='y',labelsize = 8)

        ax.tick_params(colors='#E0E0E0')
        fig.patch.set_facecolor('#080808')
        ax.spines['bottom'].set_color('#A7F500')
        ax.spines['top'].set_color('#080808')
        ax.spines['right'].set_color('#080808')
        ax.spines['left'].set_color('#080808')
        ax.set_facecolor('#080808')
        
        return plt.gcf()