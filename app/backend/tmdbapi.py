import json
import pandas as pd
import requests


class TMBDApi:
    def __init__(self, path="", get_act_and_gen=0, dataArray=None):
        if path == "":
            self.dataArray = dataArray
        else:
            self.dataArray = pd.read_csv(path)
        self.get_act_and_gen = get_act_and_gen

    def getMovieData(self):
        self.dataArray["genres"] = self.dataArray["genres"].apply(
            lambda x: [] if pd.isna(x) else eval(x)
        )
        SeriesURL = "https://api.themoviedb.org/3/search/tv?api_key=2fd4f8fec4042fda3466a92e18309708&query="
        MovieURL = "https://api.themoviedb.org/3/search/movie?api_key=2fd4f8fec4042fda3466a92e18309708&query="
        for i, row in self.dataArray.iterrows():
            title = row["title"].replace(" ", "+")
            title = title.replace("#", "")
            if row["type"] == "series":
                Series_response = requests.get(f"{SeriesURL}{title}")
                Series_data_dic = json.loads(Series_response.content)
                try:
                    result = Series_data_dic["results"][00]
                    self.dataArray.loc[i, "Release Date"] = result["first_air_date"]
                except IndexError:
                    Film_response = requests.get(f"{MovieURL}{title}")
                    Film_data_dic = json.loads(Film_response.content)
                    try:
                        result = Film_data_dic["results"][00]
                        self.dataArray.loc[i, "type"] = "film"
                        self.dataArray.loc[i, "Release Date"] = result["release_date"]
                    except IndexError:
                        continue
            else:
                Film_response = requests.get(f"{MovieURL}{title}")
                Film_data_dic = json.loads(Film_response.content)
                try:
                    result = Film_data_dic["results"][00]
                    self.dataArray.loc[i, "Release Date"] = result["release_date"]
                except IndexError:
                    Series_response = requests.get(f"{SeriesURL}{title}")
                    Series_data_dic = json.loads(Series_response.content)
                    try:
                        result = Series_data_dic["results"][00]
                        self.dataArray.loc[i, "type"] = "series"
                        self.dataArray.loc[i, "Release Date"] = result["first_air_date"]
                    except IndexError:
                        continue
            self.dataArray.loc[i, "TMBDid"] = result["id"]
            self.dataArray.at[i, "genres"] = result["genre_ids"]
            self.dataArray.loc[i, "popularity"] = result["popularity"]
        self.dataArray = self.dataArray.dropna(subset=["TMBDid"])
        if self.get_act_and_gen == 1:
            self.getGenres()

    def getActors(self):
        self.dataArray.loc[:, ("actress")] = self.dataArray.loc[:, ("actress")].apply(
            lambda x: [] if pd.isna(x) else eval(x)
        )
        ASeriesURL = "https://api.themoviedb.org/3/tv/"
        AMovieURL = "https://api.themoviedb.org/3/movie/"
        creditsURL = "/credits?api_key=2fd4f8fec4042fda3466a92e18309708"
        for i, row in self.dataArray.iterrows():
            rows = row["TMBDid"]
            if row["type"] == "series":
                url = f"{ASeriesURL}{rows}{creditsURL}"
            else:
                url = f"{AMovieURL}{rows}{creditsURL}"
            req = requests.get(url)
            actress = json.loads(req.content)
            credits = []

            for j, data in enumerate(actress["cast"]):
                if j >= 10:
                    break
                credits.append(data["name"])
            self.dataArray.at[i, "actress"] = credits

    def getGenres(self):
        genres_df = pd.read_csv("app/backend/files/Netflix/genres.csv")
        genres_dict = dict(zip(genres_df["id"], genres_df["name"]))
        for i, row in self.dataArray.iterrows():
            genres = row["genres"]
            genres_names = []
            for genre in genres:
                genres_names.append(genres_dict[genre])
            self.dataArray.at[i, "genres"] = genres_names
        self.getActors()


def get_genres(gen: list) -> str:
    with open("app/backend/files/Netflix/genres.csv", "r") as f:
        genres_df = pd.read_csv(f)
        genres_dict = dict(zip(genres_df["id"], genres_df["name"]))
        for i in range(len(gen)):
            gen[i] = genres_dict[gen[i]]
        return ", ".join(gen)


def get_actors(program_type: str, tmdbid: str) -> str:
    ASeriesURL = "https://api.themoviedb.org/3/tv/"
    AMovieURL = "https://api.themoviedb.org/3/movie/"
    creditsURL = "/credits?api_key=2fd4f8fec4042fda3466a92e18309708"
    if program_type == "series":
        url = f"{ASeriesURL}{tmdbid}{creditsURL}"
    else:
        url = f"{AMovieURL}{tmdbid}{creditsURL}"
    req = requests.get(url)
    actress = json.loads(req.content)
    credits = []
    for j, data in enumerate(actress["cast"]):
        if j >= 10:
            break
        credits.append(data["name"])
    return ", ".join(credits)


def single_movie_search(title: str) -> list:
    SeriesURL = "https://api.themoviedb.org/3/search/tv?api_key=2fd4f8fec4042fda3466a92e18309708&query="
    MovieURL = "https://api.themoviedb.org/3/search/movie?api_key=2fd4f8fec4042fda3466a92e18309708&query="
    tit = title.replace(" ", "+").replace("#", "")
    element = title.find(":")

    if element != -1:
        tit = tit[:element]
        Series_response = requests.get(f"{SeriesURL}{tit}")
        Series_data_dic = json.loads(Series_response.content)
        actors = get_actors("series", Series_data_dic["results"][00]["id"])
    else:
        Series_response = requests.get(f"{MovieURL}{tit}")
        Series_data_dic = json.loads(Series_response.content)
        actors = get_actors("movies", Series_data_dic["results"][00]["id"])
    overview = Series_data_dic["results"][00]["overview"]
    genres = get_genres(Series_data_dic["results"][00]["genre_ids"])
    return [overview, genres, actors]
