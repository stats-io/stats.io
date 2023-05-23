import json
import pandas as pd
import requests
import os

genres_path = os.path.abspath("app/backend/files/Netflix/genres.csv")

class TMBDApi:
    def __init__(self, path="", get_act_and_gen=0, data_array=None):
        if path == "":
            self.data_array = data_array
        else:
            self.data_array = pd.read_csv(path)
        self.get_act_and_gen = get_act_and_gen

    def get_movie_data(self):
        self.data_array["genres"] = self.data_array["genres"].apply(
            lambda x: [] if pd.isna(x) else eval(x)
        )
        series_url = "https://api.themoviedb.org/3/search/tv?api_key=2fd4f8fec4042fda3466a92e18309708&query="
        movie_url = "https://api.themoviedb.org/3/search/movie?api_key=2fd4f8fec4042fda3466a92e18309708&query="
        for i, row in self.data_array.iterrows():
            title = row["title"].replace(" ", "+")
            title = title.replace("#", "")
            if row["type"] == "series":
                series_response = requests.get(f"{series_url}{title}")
                series_data_dic = json.loads(series_response.content)
                try:
                    result = series_data_dic["results"][00]
                    self.data_array.loc[i, "Release Date"] = result["first_air_date"]
                except IndexError:
                    film_response = requests.get(f"{movie_url}{title}")
                    film_data_dic = json.loads(film_response.content)
                    try:
                        result = film_data_dic["results"][00]
                        self.data_array.loc[i, "type"] = "film"
                        self.data_array.loc[i, "Release Date"] = result["release_date"]
                    except IndexError:
                        continue
            else:
                film_response = requests.get(f"{movie_url}{title}")
                film_data_dic = json.loads(film_response.content)
                try:
                    result = film_data_dic["results"][00]
                    self.data_array.loc[i, "Release Date"] = result["release_date"]
                except IndexError:
                    series_response = requests.get(f"{series_url}{title}")
                    series_data_dic = json.loads(series_response.content)
                    try:
                        result = series_data_dic["results"][00]
                        self.data_array.loc[i, "type"] = "series"
                        self.data_array.loc[i, "Release Date"] = result[
                            "first_air_date"
                        ]
                    except IndexError:
                        continue
            self.data_array.loc[i, "TMBDid"] = result["id"]
            self.data_array.at[i, "genres"] = result["genre_ids"]
            self.data_array.loc[i, "popularity"] = result["popularity"]
        self.data_array = self.data_array.dropna(subset=["TMBDid"])
        if self.get_act_and_gen == 1:
            self.get_genres()

    def get_actors(self):
        self.data_array.loc[:, ("actress")] = self.data_array.loc[:, ("actress")].apply(
            lambda x: [] if pd.isna(x) else eval(x)
        )
        series_url = "https://api.themoviedb.org/3/tv/"
        movie_url = "https://api.themoviedb.org/3/movie/"
        credits_url = "/credits?api_key=2fd4f8fec4042fda3466a92e18309708"
        for i, row in self.data_array.iterrows():
            rows = row["TMBDid"]
            if row["type"] == "series":
                url = f"{series_url}{rows}{credits_url}"
            else:
                url = f"{movie_url}{rows}{credits_url}"
            req = requests.get(url)
            actress = json.loads(req.content)
            credits = []

            for j, data in enumerate(actress["cast"]):
                if j >= 10:
                    break
                credits.append(data["name"])
            self.data_array.at[i, "actress"] = credits

    def get_genres(self):
        genres_df = pd.read_csv(genres_path)
        genres_dict = dict(zip(genres_df["id"], genres_df["name"]))
        for i, row in self.data_array.iterrows():
            genres = row["genres"]
            genres_names = []
            for genre in genres:
                genres_names.append(genres_dict[genre])
            self.data_array.at[i, "genres"] = genres_names
        self.get_actors()


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
