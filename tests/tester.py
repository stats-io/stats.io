from unittest import TestLoader
from unittest import TextTestRunner

def testGeneralAll():
    import generaltests.testMainScr as mainscr
    import generaltests.testStatioApp as testapp
    import generaltests.testTmdbApi as tmdbapi

    tests = []
    tests.append(TestLoader().loadTestsFromTestCase(mainscr.TestMainScreenNB))
    tests.append(TestLoader().loadTestsFromTestCase(mainscr.TestMainScreenSB))
    tests.append(TestLoader().loadTestsFromTestCase(testapp.TestStatsApp))
    tests.append(TestLoader().loadTestsFromTestCase(tmdbapi.MovieDataUpdate))
    tests.append(TestLoader().loadTestsFromTestCase(tmdbapi.MovieGenres))
    tests.append(TestLoader().loadTestsFromTestCase(tmdbapi.MovieActors))

    runner = TextTestRunner(verbosity=2)
    for i in tests:
        runner.run(i)


def testNetflixAll():
    import netflixtests.testDataAdapter as adapter
    import netflixtests.testHistoryScr as history
    import netflixtests.testLoadingScr as loading
    import netflixtests.testNewDataScr as newdata
    import netflixtests.testUpdateData as update

    tests = []
    tests.append(TestLoader().loadTestsFromTestCase(adapter.IsAdaptedWell))
    tests.append(TestLoader().loadTestsFromTestCase(history.NetflixList))
    tests.append(TestLoader().loadTestsFromTestCase(history.NetflixSearch))
    tests.append(TestLoader().loadTestsFromTestCase(loading.LoadingisFinished))
    tests.append(TestLoader().loadTestsFromTestCase(loading.UpdateFileisvalid))
    tests.append(TestLoader().loadTestsFromTestCase(loading.GoToNetflixMainScreen))
    tests.append(TestLoader().loadTestsFromTestCase(newdata.testNetflixNewDataScreenCSV))
    tests.append(TestLoader().loadTestsFromTestCase(newdata.TestLoadingButtonPressWhenFileExsists))
    tests.append(TestLoader().loadTestsFromTestCase(newdata.TestMainButtonPressWhenFileExsists))
    tests.append(TestLoader().loadTestsFromTestCase(newdata.FormatofUserFileIsGood))
    tests.append(TestLoader().loadTestsFromTestCase(newdata.FormatofHistoryFileIsGood))
    tests.append(TestLoader().loadTestsFromTestCase(update.FormatDataTest))
    tests.append(TestLoader().loadTestsFromTestCase(update.LookintoTMBD))
    tests.append(TestLoader().loadTestsFromTestCase(update.LookintoLocalDb))
    tests.append(TestLoader().loadTestsFromTestCase(update.FetchintoLocalDb))

    runner = TextTestRunner(verbosity=2)
    for i in tests:
        runner.run(i)


def testSpotifyAll():
    import spotifytests.testHistoryScr as history
    import spotifytests.testLoadingScr as loading
    import spotifytests.testLoginScr as login
    import spotifytests.testNewDataScr as newdata
    import spotifytests.testProcessData as process

    tests = []
    tests.append(TestLoader().loadTestsFromTestCase(history.SpotifyList))
    tests.append(TestLoader().loadTestsFromTestCase(history.SpotifySearch))
    tests.append(TestLoader().loadTestsFromTestCase(loading.LoadingisFinished))
    tests.append(TestLoader().loadTestsFromTestCase(loading.UpdateFileisvalid))
    tests.append(TestLoader().loadTestsFromTestCase(loading.GoToNetflixMainScreen))
    tests.append(TestLoader().loadTestsFromTestCase(login.TestButtons))
    tests.append(TestLoader().loadTestsFromTestCase(newdata.TestProcessFile))
    tests.append(TestLoader().loadTestsFromTestCase(newdata.TestMainButtonPressWhenFileExsists))
    tests.append(TestLoader().loadTestsFromTestCase(newdata.TestLoadingButtonPressWhenFileExsists))
    tests.append(TestLoader().loadTestsFromTestCase(process.TestDataProcessing))

    runner = TextTestRunner(verbosity=2)
    for i in tests:
        runner.run(i)


if __name__ == "__main__":
    testGeneralAll()
    testNetflixAll()
    testSpotifyAll()
