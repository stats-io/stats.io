from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigationItem


class NetflixHistoryScreen(MDBottomNavigationItem):
    list_of_films = None

    def loadHistory(self, *args):
        pass

    def searchTitle(self, *args):
        pass

    def searchFiltered(self, *args):
        pass


class SpotifyHistoryScreen(MDBottomNavigationItem):
    list_of_songs = None

    def loadHistory(self, *args):
        pass

    def searchTitle(self, *args):
        pass


class MainScreen(Screen):
    def SpotifyChangeScreen(self, instance):
        pass

    def NetflixNextScreen(self, instance):
        pass


class NetflixNewDataScreen(Screen):
    file_manager = None
    history_file_path = None

    def addFile(self, instance):
        pass

    def getFile(self, instance):
        pass

    def NetflixloadingScreen(self, instance):
        pass

    def NetflixMainScreen(self, instance):
        pass


class SpotifyNewDataScreen(Screen):
    file_manager = None
    history_file_path = None

    def addFile(self, *args):
        pass

    def getFile(self, *args):
        pass

    def SpotifyMainScreen(self, *args):
        pass

    def SpotifyLoadingScreen(self, *args):
        pass


class NetflixLoadingScreen(Screen):
    finishedLoading = 0
    update = None

    def startUpdatingData(self, instance):
        pass

    def NetflixMainScreen(self, instance):
        pass


class SpotifyLoadingScreen(Screen):
    finishedLoading = 0
    update = None

    def startUpdatingData(self, instance):
        pass

    def spotifyMainScreenChange(self, instance):
        pass


class SpotifyLoginScreen(Screen):
    def spotifyMainScreenChange(self, *args):
        pass

    def handleLogin(self, *args):
        pass


class SpotifyProcessData:
    def __init__(self, *args) -> None:
        pass

    def load_history_data(self, *args):
        pass

    def load_last_fifty_tracks_data(self, *args):
        pass

    def load_json_file(self, *args):
        pass


class NetflixDataAdapter:
    csvFile = None
    data = None
    how_many_new = None
    db = None

    def remakeFile(self):
        pass


class NetflixUpdateData:
    data = None
    csvFile = None

    def formatUserData(self):
        pass

    def lookintoTMBD(self):
        pass

    def lookintoLocalDb(self):
        pass

    def fetchintoLocalDb(self):
        pass


class TMBDApi:
    dataArray = None

    def getMovieData(self):
        pass

    def getActors(self):
        pass

    def getGenres(self):
        pass


class SpotifyUserScreen(Screen):
    spotifyData = None
    historyData = None

    def changeScreen(self, name):
        pass

    def backToMainScreen(self):
        pass


class SpotifyMainScreen(MDBottomNavigationItem):
    def countMinutes(self):
        pass

    def chooseDayOdWeek(self):
        pass


class SpotifyTopListScreen(MDBottomNavigationItem):
    topArtists = None
    topTracks = None
    recommendations = None

    def createTopLists(self):
        pass


class NetflixUserScreen(Screen):
    netflixData = None

    def changeScreen(self, name):
        pass

    def retrieveDataFromDb(self):
        pass

    def backToMainScreen(self):
        pass


class NetflixMainScreen(MDBottomNavigationItem):
    def countMovies(self):
        pass

    def countSeries(self):
        pass


class NetflixChartsScreen(MDBottomNavigationItem):
    charts = None

    def createCharts(self):
        pass

    def createCardsWithCharts(self):
        pass


class NetflixTopListScreen(MDBottomNavigationItem):
    topActors = None
    topGenres = None
    topSeries = None
    mostPopularWatched = None
    leastPopularWatched = None

    def findTop(self):
        pass

    def createTopLists(self):
        pass


class setUp(MDApp):
    def build(self):
        Main_Screen = MainScreen(name="Main_Screen")
        Netflix_New_Data_Screen = NetflixNewDataScreen(name="Netflix_New_Data_Screen")
        Spotify_New_Data_Screen = SpotifyNewDataScreen(name="Spotify_New_Data_Screen")
        Netflix_Loading_Screen = NetflixLoadingScreen(name="Netflix_Loading_Screen")
        Netflix_Main_Screen = NetflixMainScreen(name="Netflix_Main_Screen")
        Spotify_Login_Screen = SpotifyLoginScreen(name="Spotify_Login_Screen")
        Spotify_Loading_Screen = SpotifyLoadingScreen(name="Spotify_Loading_Screen")

        screen_manager = ScreenManager()
        screen_manager.add_widget(Main_Screen)
        screen_manager.add_widget(Netflix_New_Data_Screen)
        screen_manager.add_widget(Spotify_New_Data_Screen)
        screen_manager.add_widget(Netflix_Loading_Screen)
        screen_manager.add_widget(Netflix_Main_Screen)
        screen_manager.add_widget(Spotify_Login_Screen)
        screen_manager.add_widget(Spotify_Loading_Screen)

        return screen_manager
