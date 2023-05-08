import json
import datetime
import pandas as pd
import numpy as np
import requests

class TMBDApi:

    def __init__(self, path = None, get_act_and_gen = 0, daAtarray = None):
        if path == '':
            self.dataArray = daAtarray
        else:
            self.dataArray = pd.read_csv(path)
        self.get_act_and_gen = get_act_and_gen

    def getMovieData(self):
        self.dataArray['genres'] = self.dataArray['genres'].apply(lambda x: [] if pd.isna(x) else eval(x))

        SeriesURL = "https://api.themoviedb.org/3/search/tv?api_key=2fd4f8fec4042fda3466a92e18309708&query="
        MovieURL = f"https://api.themoviedb.org/3/search/movie?api_key=2fd4f8fec4042fda3466a92e18309708&query="

        for i, row in self.dataArray.iterrows():
            title = row['title'].replace(' ','+')
            title = title.replace('#',"")
            if row['type'] == 'series':
                Series_response = requests.get(f'{SeriesURL}{title}')
                Series_data_dic = json.loads(Series_response.content)
                try:
                    result = Series_data_dic['results'][00]
                except IndexError:
                    Film_response = requests.get(f'{MovieURL}{title}')
                    Film_data_dic = json.loads(Film_response.content)
                    try:
                        result = Film_data_dic['results'][00]
                        self.dataArray.loc[i,'type'] = 'film'
                    except IndexError:
                        continue
            else:
                Film_response = requests.get(f'{MovieURL}{title}')
                Film_data_dic = json.loads(Film_response.content)
                try:
                    result = Film_data_dic['results'][00]
                except IndexError:
                    Series_response = requests.get(f'{SeriesURL}{title}')
                    Series_data_dic = json.loads(Series_response.content)
                    try:
                        result = Series_data_dic['results'][00]
                        self.dataArray.loc[i,'type'] = 'series'
                    except IndexError:
                        continue

            self.dataArray.loc[i, 'TMBDid'] = result['id']
            self.dataArray.at[i, 'genres'] = result['genre_ids']
            self.dataArray.loc[i, 'popularity'] = result['popularity']
        self.dataArray = self.dataArray.dropna(subset=['TMBDid'])
        if self.get_act_and_gen == 1:
            self.getGenres()

    def getActors(self):
        self.dataArray.loc[:,('actress')] = self.dataArray.loc[:,('actress')].apply(lambda x: [] if pd.isna(x) else eval(x))

        SeriesURL = "https://api.themoviedb.org/3/tv/"
        MovieURL = "https://api.themoviedb.org/3/movie/"
        creditsURL = "/credits?api_key=2fd4f8fec4042fda3466a92e18309708"

        for i, row in self.dataArray.iterrows():
            if row['type'] == 'series':
                url = f"{SeriesURL}{row['TMBDid']}{creditsURL}"
            else:
                url = f"{MovieURL}{row['TMBDid']}{creditsURL}"
            req = requests.get(url)
            actress = json.loads(req.content)
            credits = []

            for j,data in enumerate(actress['cast']):
                if j >= 10:
                    break
                credits.append(data['name'])
            self.dataArray.at[i,'actress'] = credits

    def getGenres(self):

        genres_df = pd.read_csv('./genres.csv')
        genres_dict = dict(zip(genres_df['id'], genres_df['name']))
        for i, row in self.dataArray.iterrows():
            genres = row['genres']
            genres_names = []
            for genre in genres:
                genres_names.append(genres_dict[genre])
            self.dataArray.at[i, 'genres'] = genres_names
        self.getActors()
