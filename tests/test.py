import unittest
from read_env_keys import *
from theoddsapi.api import *


class TestTheOddsAPI(unittest.TestCase):
    def setUp(self):
        print("\nOS cwd: ", os.getcwd())
        api_key = read_key_from_env('api_key.env')
        print("API Key: ", api_key)
        self.client = theOddsAPI(api_key)
        self.api_key = api_key

    def _assert_json(self, response):
        # Deserialization of response gets a Python list or a dictionary.
        print("Response: ", response)
        assert isinstance(
            response, dict) or isinstance(response, list), f"list or dict expected, got: {type(response)}"


class TestGetSports(TestTheOddsAPI):

    def test_get_sports(self):
        params = {
            'apiKey': self.api_key}
        response = self.client.get_sports(params)
        self._assert_json(response)


class TestGetOdds(TestTheOddsAPI):

    def test_get_odds(self):
        pass


class TestGetScores(TestTheOddsAPI):

    def _test_get_scores(self, **kwargs):
        """Helper function to test get_scores

        Parameters
        ----------
        sport : str
            Sport key for which to return games and odds

        days_from : str
            The number of days in the past from which to return completed games.
             Valid values are integers from 1 to 3. If this field is missing,
              only live and upcoming games are returned.
        """
        params = kwargs
        params['sport'] = kwargs['sport']
        params['apiKey'] = self.api_key
        response = self.client.get_scores('basketball_nba', params)
        self._assert_json(response)

    def test_get_scores(self):
        self._test_get_scores(sport='basketball_nba',
                              daysFrom=3,
                              dateFormat='iso')
        self._test_get_scores(sport='basketball_nba',
                              daysFrom=2,
                              dateFormat='iso')
        self._test_get_scores(sport='basketball_nba')


class TestGetHistoricalOdds(TestTheOddsAPI):
    REGIONS = ['uk', 'us', 'eu', 'au']
    MARKETS = ['h2h', 'spreads', 'totals', 'outrights']
    DATES = ['2023-02-01T12:15:00Z']
    DATE_FORMAT = ['iso', 'unix']
    ODDS_FORMAT = ['decimal', 'american']
    EVENT_IDS = [None]
    BOOKMAKERS = ['FanDuel', 'DraftKings']

    def _test_get_historical_odds(self, **kwargs):
        """Helper function to test get_historical_odds

           Parameters
           ----------
           sport : str
               Sport key for which to return games and odds. Obtained from the
                /sports endpoint
           regions : str
               Which bookmakers to appear in the response.
           markets : str
               The odds market to return.
           date : str
               The timestamp of the data snapshot to be returned, specified in 
               ISO8601 format. Closest snapshot equal to or earlier than date 
               provided will be returned.
           eventIds : list[str]
               Comma-separated game ids. Filters the response to only return 
               games for the specified game ids, provided those games have not 
               expired.
           bookmakers : list[int]
               The bookmaker(s) to be returned. Every group of 10 bookmakers 
               counts as 1 request.
           """
        params = kwargs
        params['apiKey'] = self.api_key
        sport = params['sport']
        del params['sport']
        print(params)

        response = self.client.get_historical_odds(sport, params)
        self._assert_json(response)

    def test_get_historical_odds_h2h(self):
        self._test_get_historical_odds(
            sport='basketball_nba',
            regions='us',
            markets='h2h',
            date='2023-02-15T12:00:00Z',
            bookmakers='fanduel',
            oddsFormat='american',
            eventIds='0363b83afb7b3532a0ee4682512d3c11')

    def test_get_historical_odds_spreads(self):
        self._test_get_historical_odds(
            sport='basketball_nba',
            regions='us',
            markets='spreads',
            date='2023-01-01T12:00:00Z',
            bookmakers='fanduel',
            oddsFormat='american')

    def test_get_historical_odds_totals(self):
        self._test_get_historical_odds(
            sport='basketball_nba',
            regions='us',
            markets='totals',
            date='2023-01-01T12:00:00Z',
            bookmakers='fanduel',
            oddsFormat='american')

    def test_get_historical_odds_outrights(self):
        self._test_get_historical_odds(
            sport='basketball_nba',
            regions='us',
            markets='outrights',
            date='2023-01-01T12:00:00Z',
            bookmakers='fanduel',
            oddsFormat='american')


class TestGetEventOdds(TestTheOddsAPI):

    def _test_get_event_odds(self, **kwargs):
        """Helper function to test get_event_odds

        Parameters
        ----------
        sport : str
            Sport key for which to return games and odds. Obtained from the
            /sports endpoint
        regions : str
            Which bookmakers to appear in the response.
        markets : str
            The odds market to return.
        eventId : list[str]
            Comma-separated game ids. Filters the response to only return 
            games for the specified game ids, provided those games have not 
            expired.
        bookmakers : list[int]
            The bookmaker(s) to be returned. Every group of 10 bookmakers 
            counts as 1 request.
        """
        event_id = kwargs['eventId']
        sport = kwargs['sport']
        params = kwargs
        params['apiKey'] = self.api_key
        del params['sport']
        del params['eventId']
        print(params)

        response = self.client.get_event_odds(sport, event_id, params)
        self._assert_json(response)

    def test_get_event_odds_nba(self):
        self._test_get_event_odds(
            sport='basketball_nba',
            regions='us',
            markets='h2h',
            eventId='4afb8f0ba6e00d9e44b4240d1ba5493c',
            bookmakers='fanduel')

    def test_get_event_odds_nfl(self):
        pass


class TestGetUsageQuotas(TestTheOddsAPI):

    def test_get_requests_remaining(self):
        requests_remaining = self.client.get_requests_remaining()
        assert isinstance(requests_remaining, int)

    def test_get_requests_used(self):
        requests_used = self.client.get_requests_used()
        assert isinstance(requests_used, int)


if __name__ == '__main__':
    historical_odds_suite = unittest.TestSuite()
    historical_odds_suite.addTest(
        TestGetHistoricalOdds('test_get_historical_odds_h2h'))
    historical_odds_suite.addTest(
        TestGetHistoricalOdds('test_get_historical_odds_spreads'))
    historical_odds_suite.addTest(
        TestGetHistoricalOdds('test_get_historical_odds_totals'))
    historical_odds_suite.addTest(TestGetHistoricalOdds(
        'test_get_historical_odds_outrights'))

    event_odds_suite = unittest.TestSuite()
    event_odds_suite.addTest(TestGetEventOdds('test_get_event_odds_nba'))

    runner = unittest.TextTestRunner()
    runner.run(event_odds_suite)
