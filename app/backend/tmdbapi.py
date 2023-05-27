import json
import pandas as pd
import requests
import os

import time

import threading

genres_path = os.path.abspath("app/backend/netflix/database/genres.csv")

class TMBDApi:
    def __init__(self, path="", get_act_and_gen=0, data_array=None):
        if path == "":
            self.data_array = data_array
        else:
            self.data_array = pd.read_csv(path, encoding='utf-8')
        self.get_act_and_gen = get_act_and_gen
        
    def __get_movie_data(self, title):
        url = "https://api.themoviedb.org/3/search/movie?api_key=2fd4f8fec4042fda3466a92e18309708&query="
        response = json.loads((requests.get(f"{url}{title}")).content)
        try:
            res = response["results"][00]
            return ("film", str(res["id"]), res["genre_ids"], res["popularity"], res["release_date"])
        except IndexError:
            None
    
    def __get_series_data(self, title):
        url = "https://api.themoviedb.org/3/search/tv?api_key=2fd4f8fec4042fda3466a92e18309708&query="
        response = json.loads((requests.get(f"{url}{title}")).content)
        try:
            res = response["results"][00]
            return ("series", str(res["id"]), res["genre_ids"], res["popularity"], res["first_air_date"])
        except IndexError:
            return None

    def __get_title_data(self, title, type, index):
        title = title.replace(" ", "+").replace("#", "")
        result = None
        if type == "film":
            result = self.__get_movie_data(title)
            if not result:
                result = self.__get_series_data(title)
        else:
            result = self.__get_series_data(title)
            if not result:
                result = self.__get_movie_data(title)
        if result == None:
            return
        lst = self.movies_list[index]
        lst["type"], lst["TMBDid"], lst["genres"], lst["popularity"], lst["Release Date"] = result
        

    def get_movie_data(self):
        self.data_array["genres"] = self.data_array["genres"].apply(
            lambda x: [] if pd.isna(x) else eval(x)
        )
        
        self.movies_list = []
        for _, row in self.data_array.iterrows():
            hashmap = {key: value.replace('\xa0', ' ') if isinstance(value, str) else value for key, value in row.items()}
            self.movies_list.append(hashmap)

        for index in range(len(self.movies_list) // 4):
            threads = [threading.Thread(target=self.__get_title_data, args=(self.movies_list[index * 4 + i]["title"], self.movies_list[index * 4 + i]["type"], index * 4 + i)) for i in range(4)]
            for i in range(4):
                threads[i].start()
            for i in range(4):
                threads[i].join()

        self.data_array = pd.DataFrame(self.movies_list)
        self.data_array = self.data_array.dropna(subset=["TMBDid"])
        if self.get_act_and_gen == 1:
            self.get_actors_genres()

    def get_actors_genres(self):
        self.__get_genres()
        self.__get_actors()

    def __get_actors(self):
        self.data_array.loc[:, ("actress")] = self.data_array.loc[:, ("actress")].apply(
            lambda x: [] if pd.isna(x) else eval(x)
        )
        series_url = "https://api.themoviedb.org/3/tv/"
        movie_url = "https://api.themoviedb.org/3/movie/"
        credits_url = "/credits?api_key=2fd4f8fec4042fda3466a92e18309708"
        
        for i, row in self.data_array.iterrows():
            tmdb_id = row["TMBDid"]
            if row["type"] == "series":
                url = f"{series_url}{tmdb_id}{credits_url}"
            else:
                url = f"{movie_url}{tmdb_id}{credits_url}"
            req = requests.get(url)
            actress = json.loads(req.content)
            credits = []

            for j, data in enumerate(actress["cast"]):
                if j >= 10:
                    break
                credits.append(data["name"])
            self.data_array.at[i, "actress"] = credits

    def __get_genres(self):
        genres_df = pd.read_csv(genres_path)
        genres_dict = dict(zip(genres_df["id"], genres_df["name"]))
        for i, row in self.data_array.iterrows():
            genres = row["genres"]
            genres_names = []
            for genre in genres:
                genres_names.append(genres_dict[genre])
            self.data_array.at[i, "genres"] = genres_names


def get_genres(gen: list) -> str:
    with open(genres_path, "r") as f:
        genres_df = pd.read_csv(f)
        genres_dict = dict(zip(genres_df["id"], genres_df["name"]))
        for i in range(len(gen)):
            gen[i] = genres_dict[gen[i]]
        return ", ".join(gen)


def get_actors(program_type: str, tmdbid: str) -> str:
    series_url = "https://api.themoviedb.org/3/tv/"
    movie_url = "https://api.themoviedb.org/3/movie/"
    credits_url = "/credits?api_key=2fd4f8fec4042fda3466a92e18309708"
    if program_type == "series":
        url = f"{series_url}{tmdbid}{credits_url}"
    else:
        url = f"{movie_url}{tmdbid}{credits_url}"
    req = requests.get(url)
    actress = json.loads(req.content)
    credits = []
    for j, data in enumerate(actress["cast"]):
        if j >= 10:
            break
        credits.append(data["name"])
    return ", ".join(credits)


def single_movie_search(title: str) -> list:
    series_url = "https://api.themoviedb.org/3/search/tv?api_key=2fd4f8fec4042fda3466a92e18309708&query="
    movie_url = "https://api.themoviedb.org/3/search/movie?api_key=2fd4f8fec4042fda3466a92e18309708&query="
    tit = title.replace(" ", "+").replace("#", "")
    element = title.find(":")

    if element != -1:
        tit = tit[:element]
        series_response = requests.get(f"{series_url}{tit}")
        series_data_dic = json.loads(series_response.content)
        actors = get_actors("series", series_data_dic["results"][00]["id"])
    else:
        series_response = requests.get(f"{movie_url}{tit}")
        series_data_dic = json.loads(series_response.content)
        actors = get_actors("movies", series_data_dic["results"][00]["id"])
    overview = series_data_dic["results"][00]["overview"]
    genres = get_genres(series_data_dic["results"][00]["genre_ids"])
    return [overview, genres, actors]
