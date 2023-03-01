import unittest
from read_env_keys import read_key_from_env
from theoddsapi import TheOddsAPI
import sys


class TestTheOddsAPI(unittest.TestCase):
    def setUp(self):
        api_key = read_key_from_env('api_key.env')
        self.client = TheOddsAPI(api_key)
        self.api_key = api_key

    def _assert_json(self, response):
        # Deserialization of response gets a Python list or a dictionary.
        # print("Response: ", response)
        assert isinstance(
            response, dict) or isinstance(response, list), f"list or dict expected, got: {type(response)}"


class TestGetSports(TestTheOddsAPI):

    def test_get_sports(self):
        response = self.client.get_sports()
        self._assert_json(response)


class TestGetOdds(TestTheOddsAPI):

    def _test_get_odds(self, **kwargs):
        """Helper function to test get_odds

            Parameters
            ----------
            sport : str
                Sport key for which to return games and odds. Obtained from the
                /sports endpoint
            regions : str
                Which bookmakers to appear in the response.
            markets : str
                The odds market to return.
            eventId : str
                Comma-separated game id(s) of upcoming or live game(s). Filters the
                response to only return games for the specified game ids, provided
                those games have not expired.
            bookmakers : str
                Comma delimited list of bookmaker(s) to be returned. Every group of
                10 bookmakers counts as 1 request.
        """
        response = self.client.get_odds(**kwargs)
        self._assert_json(response)

    def test_get_odds_h2h(self):
        self._test_get_odds(
            sport='basketball_nba',
            regions='us',
            markets='h2h',
            bookmakers='fanduel',
            oddsFormat='american')
        print('Successfully got head-to-head odds...')

    def test_get_odds_spreads(self):
        self._test_get_odds(
            sport='basketball_nba',
            regions='us',
            markets='spreads',
            bookmakers='fanduel',
            oddsFormat='american')
        print('Successfully got spread odds...')

    def test_get_odds_totals(self):
        self._test_get_odds(
            sport='basketball_nba',
            regions='us',
            markets='totals',
            bookmakers='fanduel',
            oddsFormat='american')
        print('Successfully got totals odds...')


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
        dateFormat : str
            Determines the format of timestamps in the response. Valid values
            are unix and iso (ISO 8601). By default, iso.
        """
        response = self.client.get_scores(**kwargs)
        self._assert_json(response)

    def test_get_scores(self):
        self._test_get_scores(sport='basketball_nba',
                              daysFrom=3)
        self._test_get_scores(sport='basketball_nba',
                              daysFrom=2,
                              dateFormat='iso')
        self._test_get_scores(sport='basketball_nba',
                              dateFormat='unix')
        self._test_get_scores(sport='basketball_nba')
        print('Successfully got scores...')


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
           eventId : str
                Comma-separated game id(s) of upcoming or live game(s). Filters the
                response to only return games for the specified game ids, provided
                those games have not expired.
           bookmakers : list[int]
                The bookmaker(s) to be returned. Every group of 10 bookmakers 
                counts as 1 request.
        """
        response = self.client.get_historical_odds(**kwargs)
        self._assert_json(response)

    def test_get_historical_odds_h2h(self):
        self._test_get_historical_odds(
            sport='basketball_nba',
            regions='us',
            markets='h2h',
            date='2023-02-15T12:00:00Z',
            bookmakers='fanduel',
            oddsFormat='american',
            eventId='0363b83afb7b3532a0ee4682512d3c11')
        print('Successfully got historical head-to-head odds...')

    def test_get_historical_odds_spreads(self):
        self._test_get_historical_odds(
            sport='basketball_nba',
            regions='us',
            markets='spreads',
            date='2023-01-01T12:00:00Z',
            bookmakers='fanduel',
            oddsFormat='american')
        print('Successfully got historical spread odds...')

    def test_get_historical_odds_totals(self):
        self._test_get_historical_odds(
            sport='basketball_nba',
            regions='us',
            markets='totals',
            date='2023-01-01T12:00:00Z',
            bookmakers='fanduel',
            oddsFormat='american')
        print('Successfully got historical totals odds...')


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
        eventId : str
            Comma-separated game id(s) of upcoming or live game(s). Filters the
            response to only return games for the specified game ids, provided
            those games have not expired.
        bookmakers : list[int]
            The bookmaker(s) to be returned. Every group of 10 bookmakers 
            counts as 1 request.
        """

        response = self.client.get_event_odds(**kwargs)
        self._assert_json(response)

    def test_get_event_odds_nba(self):
        # Get a valid eventId. Note that the eventId must be upcoming or live.
        odds_response = self.client.get_odds(sport='basketball_nba',
                                             regions='us',
                                             markets='h2h',
                                             daysFrom=3,
                                             bookmakers='fanduel')

        upcoming_eventId = odds_response[0]['id']

        self._test_get_event_odds(
            sport='basketball_nba',
            regions='us',
            markets='h2h',
            eventId=upcoming_eventId,
            bookmakers='fanduel')
        print(
            'Successfully got head-to-head event odds for event {upcoming_eventId}...')


class TestGetUsageQuotas(TestTheOddsAPI):

    def test_get_requests_remaining(self):
        requests_remaining = self.client.get_requests_remaining()
        assert isinstance(requests_remaining, int)
        assert requests_remaining >= 0
        print('Successfully got requests remaining...')
        print(f'{requests_remaining} requests remaining...')

    def test_get_requests_used(self):
        requests_used = self.client.get_requests_used()
        print(requests_used)
        assert isinstance(requests_used, int)
        assert requests_used >= 0
        print('Successfully got requests used...')
        print(f'{requests_used} requests used...')


if __name__ == '__main__':

    # Instantiate a client to get usage quota information after calls to tests
    api_key = read_key_from_env('./api_key.env')
    client = TheOddsAPI(api_key)

    # TestGetSports suite
    sports_suite = unittest.TestSuite()
    sports_suite.addTest(
        TestGetSports('test_get_sports')
    )

    # TestGetOdds suite
    odds_suite = unittest.TestSuite()
    odds_suite.addTest(
        TestGetOdds('test_get_odds_h2h')
    )
    odds_suite.addTest(
        TestGetOdds('test_get_odds_spreads')
    )
    odds_suite.addTest(
        TestGetOdds('test_get_odds_totals')
    )

    # TestGetHistoricalOdds suite
    historical_odds_suite = unittest.TestSuite()
    historical_odds_suite.addTest(
        TestGetHistoricalOdds('test_get_historical_odds_h2h'))
    historical_odds_suite.addTest(
        TestGetHistoricalOdds('test_get_historical_odds_spreads'))
    historical_odds_suite.addTest(
        TestGetHistoricalOdds('test_get_historical_odds_totals'))

    # TestGetEventOdds suite
    event_odds_suite = unittest.TestSuite()
    event_odds_suite.addTest(TestGetEventOdds('test_get_event_odds_nba'))

    # TestGetScores suite
    scores_suite = unittest.TestSuite()
    scores_suite.addTest(TestGetScores('test_get_scores'))

    # TestGetUsageQuotas suite
    usage_suite = unittest.TestSuite()
    usage_suite.addTest(TestGetUsageQuotas('test_get_requests_remaining'))
    usage_suite.addTest(TestGetUsageQuotas('test_get_requests_used'))

    # Set up suite runner
    runner = unittest.TextTestRunner()

    # Get suites to run from the sys args provided
    args = sys.argv[1:]
    # If any args are passed, run only the specific test suites passed
    sysarg_to_suite_dict = {
        'sports': sports_suite,
        'odds': odds_suite,
        'event_odds': event_odds_suite,
        'historical_odds': historical_odds_suite,
        'scores': scores_suite,
        'usage_quota': usage_suite,
    }
    if args:
        for arg_suite in args:
            runner.run(sysarg_to_suite_dict[arg_suite])
    # If none sys args are passed, run all test suites
    else:
        # All Suites
        for arg_suite in sysarg_to_suite_dict.keys():
            prev_requests_used = client.get_requests_used()
            runner.run(sysarg_to_suite_dict[arg_suite])
