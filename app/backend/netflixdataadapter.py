import json
import datetime
import pandas as pd
import numpy as np
import requests

class NetflixDataAdapter:

    def __init__(self,path):
        self.csvFile = path

    def remakeFile(self):
        if self.csvFile.endswith('.csv'):
            self.remakeFileLong()
        else:
            self.remakeFileShort()

    def GetTotalTime(self,data):
        self.title = {}
        self.title_final = {}
        for row in data.iterrows():
            time_str = row[1][2]
            time = datetime.datetime.strptime(time_str, '%H:%M:%S').time()
            time_in_seconds = int((time.hour * 60 + time.minute) * 60 + time.second)
            key = row[1][4]
            if key in self.title:
                self.title[key] += time_in_seconds
            else:
                self.title[key] = time_in_seconds

        for key, value in self.title.items():
            vkey = key.split(':')[0]
            if vkey in self.title_final:
                self.title_final[vkey] += self.title[key]
            else:
                self.title_final[vkey] = self.title[key]
        return self.title_final

    def FilmOrSeries(self,data):
        self.film_tab = {}
        self.series_tab = {}
        for row in data.iterrows():
            title = row[1][4]
            if ':' in title:
                self.type = 'series'
                title = row[1][4].split(':')[0]
                self.series_tab[title] = self.series_tab.get(title, 0) + 1
            else:
                self.type = 'film'
                self.film_tab[title] = self.film_tab.get(title, 0) + 1
        return self.film_tab, self.series_tab

    def GetData(self,data):
        self.title = {}
        for row in data.iterrows():
            title = row[1][4].split(':')[0]
            date = row[1][1].split(' ')[0]
            if title in self.title:
                self.title[title].append(date)
            else:
                self.title[title] = []
                self.title[title].append(date)
        self.title_final = {}
        for key, value in self.title.items():
            name = key.split(':')[0]
            if name in self.title_final:
                self.title_final[name].append(self.title[key])
            else:
                self.title_final[name] = []
                self.title_final[name].append(self.title[key])
        return self.title_final

    def remakeFileLong(self):
        self.data = pd.read_csv(self.csvFile)
        self.data = self.data.loc[self.data['Supplemental Video Type'].isna()]
        self.TotalData = self.GetData(self.data)
        self.TotalTime = self.GetTotalTime(self.data)
        self.film_ep , self.series_ep = self.FilmOrSeries(self.data)
        self.adapted_data = []
        for key, value in self.film_ep.items():
            new = ({'title': f'{key}', 'type': 'film', 'number_of_episodes': value, 'SumOfTime': self.TotalTime[key], 'Dates': self.TotalData[key]})
            self.adapted_data.append(new)
        for key, value in self.series_ep.items():
            new = ({'title': f'{key}', 'type': 'series', 'number_of_episodes': value, 'SumOfTime': self.TotalTime[key], 'Dates': self.TotalData[key]})
            self.adapted_data.append(new)

        self.df = pd.DataFrame(self.adapted_data)
        self.df.to_csv('adapted_data.csv', index=False)
        self.csvFile = 'adapted_data.csv'


    def remakeFileShort(self):
        self.tab = []
        self.dic_of_film = {}
        self.dic_of_series = {}

        with open(self.csvFile, 'r') as f:
            for line in f.readlines():
                line = line.split(':')[0]
                if ',' in line:
                    self.type = 'film'
                    line = line.split(',')[0]
                    self.dic_of_film[line] = self.dic_of_film.get(line, 0) + 1
                else:
                    self.type = 'series'
                    self.dic_of_series[line] = self.dic_of_series.get(line, 0) + 1

            for key, value in self.dic_of_film.items():
                new = ({'title': f'{key}', 'type': 'film', 'number_of_episodes': value})
                self.tab.append(new)

            for key, value in self.dic_of_series.items():
                new = ({'title': f'{key}', 'type': 'series', 'number_of_episodes': value})
                self.tab.append(new)

        self.df = pd.DataFrame(self.tab)
        self.df.insert(3, 'SumOfTime', value=np.nan)
        self.df.insert(4, 'Dates', value=np.nan)
        self.df.to_csv('adapted_data.csv', index=False)
        self.csvFile = 'adapted_data.csv'
