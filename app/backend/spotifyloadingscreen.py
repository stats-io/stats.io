import spotifyproccesdata as PD


class SpotifyLoadingScreen:
    def __init__(self):
        self.finished_loading = 0

    def startProcessingData(self):
        x = PD.SpotifyProcessData()
        x.ProcessDataFromFile()
        self.finished_loading = 1

