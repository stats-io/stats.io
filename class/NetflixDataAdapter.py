import json
from ast import literal_eval
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

    def remakeFileLong(self):
        self.data = pd.read_csv(self.csvFile)
        self.data = self.data[['Duration', 'Title']]
        self.data = self.data.rename(columns={'Duration': 'SumOfTime', 'Title': 'title'})
        self.data['SumOfTime'] = pd.to_timedelta(self.data['SumOfTime'].astype(str)).dt.total_seconds()
        self.data['row_num'] = range(len(self.data))
        self.data = self.data.groupby('title', sort=False)[['SumOfTime', 'row_num']].sum().reset_index()
        self.data = self.data.sort_values('row_num').drop('row_num', axis=1)
        self.data.to_csv('kotek.csv', index=False)


    def remakeFileShort(self):
        self.tab = []
        self.dic_of_film = {}
        self.dic_of_series = {}

        with open('./user_file', 'r') as f:
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
                new = ({'title': f'{key}', 'type': 'film', 'number_of_episodes': f'{value}'})
                self.tab.append(new)

            for key, value in self.dic_of_series.items():
                new = ({'title': f'{key}', 'type': 'series', 'number_of_episodes': f'{value}'})
                self.tab.append(new)

        self.df = pd.DataFrame(self.tab)
        self.df.insert(3, 'SumOfTime', value=np.nan)
        self.df.to_csv('adapted_data2.csv', index=False)
        self.csvFile = 'adapted_data2.csv'
