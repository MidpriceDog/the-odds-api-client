import requests
import pandas as pd
from bs4 import BeautifulSoup


class TheOddsAPI(object):
    """
    This module provides functions to get historical snapshots of sports odds 
    data back to 2020 as well as game scores and results for past and live games.
    """

    HOST = "https://api.the-odds-api.com"
    # List of bookmaker regions to scrape from the-odds-api.com
    # NOTE: Index of bookmaker regions reflects the index of the table on the website to scrape
    BOOKMAKER_REGIONS = ['all', 'us', 'uk', 'eu', 'au']

    def _get(self, host, endpoint, params):
        """Helper function for GET requests to The Odds API server

        Parameters
        ----------
        host : str
            The host used by all requests
        endpoint : str
            A valid endpoint to make a request to.
            See https://the-odds-api.com/liveapi/guides/v4/ for a comprehensive
            list.
        params : dict
            Valid parameters to pass as part of GET requests to various
            endpoints. See https://app.swaggerhub.com/apis-docs/the-odds-api/odds-api/4
            for a comprehensive list.
        Returns
        -------
        dict or None
            Returns response from server if successful; otherwise, returns None
        """

        params['apiKey'] = self.api_key

        response = requests.get(host + endpoint, params=params)

        if response.status_code != 200:
            print(
                f'Failed to get {endpoint}: status_code {response.status_code}, response body {response.text}')
            return None
        else:
            return response.json()

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_sports(self, all: str = 'false'):
        """Get list of available sports and tournaments

        Parameters
        ----------
        all : bool, optional
            When excluded, only recently updated (in-season) sports appear.
            Include this paramter to see all available sports, by default false.
        """
        params = {
            'all': all
        }
        endpoint = f"/v4/sports/"
        sports_response = self._get(TheOddsAPI.HOST, endpoint, params)
        return sports_response

    def _get_usage_quota_helper(self):
        """Helper function for getting requests used and requests remaining

        Returns
        -------
        Response
            response object from GET request to the /v4/sports endpoint which
            does not affect the usage quota
        """
        # Make a request that does not affect the usage quota
        params = dict()
        endpoint = f"/v4/sports/"
        response = self.get_sports()
        params['apiKey'] = self.api_key
        # Do NOT return the json of the response because we will need the headers
        response = requests.get(TheOddsAPI.HOST + endpoint, params=params)
        return response

    def get_requests_remaining(self):
        """Get the number of requests remaining for current month

        Returns
        -------
        int
            Number of requests remaining for current month
        """
        usage_response = self._get_usage_quota_helper()
        return int(usage_response.headers['x-requests-remaining'])

    def get_requests_used(self):
        """Get the number of requests used in current month

        Returns
        -------
        int
            Number of requests used in current month
        """
        usage_response = self._get_usage_quota_helper()
        return int(usage_response.headers['x-requests-used'])

    def get_odds(self, **kwargs):
        """Returns a list of upcoming and live games with recent odds for a
         given sport, region and market

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
        # Create the query parameters from the kwargs
        params = kwargs
        sport = params['sport']
        del params['sport']
        endpoint = f'/v4/sports/{sport}/odds'
        odds_response = self._get(TheOddsAPI.HOST, endpoint, params)
        return odds_response

    def get_scores(self, **kwargs):
        """Returns a list of upcoming, live and recently completed games for a
        given sport. Live and recently completed games contain scores. Games
        from up to 3 days ago can be returned using the daysFrom parameter.
        Live scores update approximately every 30 seconds.

        Parameters
        ----------
        sport : str
            Sport key for which to return games and odds. See list of covered
            sports at https://the-odds-api.com/sports-odds-data/sports-apis.html
        daysFrom : int
            The number of days in the past from which to return completed games.
            Valid values are integers from 1 to 3. If this field is missing,
            only live and upcoming games are returned.
        dateFormat : str
            Determines the format of timestamps in the response. Valid values
            are unix and iso (ISO 8601). By default, iso.
        """
        # params will have the key 'daysFrom' if it is supplied.
        # Otherwise, empty dict.
        params = kwargs
        sport = params['sport']
        del params['sport']
        endpoint = f'/v4/sports/{sport}/scores/'
        scores_response = self._get(TheOddsAPI.HOST, endpoint, params)
        return scores_response

    def get_historical_odds(self, **kwargs):
        """Returns a snapshot of games with bookmaker odds for a given sport, region
         and market, at a given historical date. Historical odds data is available
          from June 6th 2020, with snapshots taken at 10 minute intervals. From
          September 2022, historical odds snapshots are available at 5 minute
          intervals. The historical odds endpoint is only available on paid
          usage plans at this time.

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
        bookmakers : str
            Comma delimited list of bookmaker(s) to be returned. Every group of
            10 bookmakers counts as 1 request.
        """
        # Create the query parameters from the kwargs
        params = kwargs
        sport = params['sport']
        del params['sport']
        # Create the endpoint from the kwargs
        endpoint = f'/v4/sports/{sport}/odds-history/'

        odds_history_response = self._get(TheOddsAPI.HOST, endpoint, params)
        return odds_history_response

    def get_event_odds(self, **kwargs):
        """Returns odds for a single game. Accepts any available betting markets
        using the markets parameter. To get available markets info, use
        get_featured_betting_markets, get_additonal_markets, or get_player_props
        endpoint.

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
        # Create the query parameters from the kwargs
        params = kwargs
        sport = params['sport']
        event_id = params['eventId']
        del params['sport']
        del params['eventId']
        # Create the endpoint from the kwargs
        endpoint = f'/v4/sports/{sport}/events/{event_id}/odds/'
        event_odds_response = self._get(
            TheOddsAPI.HOST, endpoint, params)
        return event_odds_response

    @staticmethod
    def get_featured_betting_markets():
        """Get the most common markets that are featured by bookmakers.
        Terminology for betting markets can vary by country, sport and even
        amongst bookmakers.

        Returns
        -------
        pd.DataFrame
            Dataframe of featured betting markets listed at
             https://the-odds-api.com/sports-odds-data/betting-markets.html
        """
        featured_betting_markets_dict = {
            'market_key': ['h2h', 'spreads', 'totals', 'outrights', 'h2h_lay', 'outrights_lay'],
            'market_names': ['Head to head, Moneyline', 'Points spread, Handicap',
                             'Total points/goals, Over/Under', 'Outrights, Futures',
                             'Head to head, Moneyline', 'Outrights, Futures'],
            'description': [
                'Bet on the winning team or player of a game (includes the draw for soccer)',
                'The spreads market as featured by a bookmaker. Bet on the winning team after a points handicap has been applied to each team',
                'The totals market as featured by a bookmaker. Bet on the total score of the game being above or below a threshold',
                'Bet on a final outcome of a tournament or competition',
                'Bet against a h2h outcome. This market is only applicable to betting exchanges',
                'Bet against an outrights outcome. This market is only applicable to betting exchanges'
            ]
        }
        return pd.DataFrame(featured_betting_markets_dict)

    @staticmethod
    def get_additional_markets():
        """Get information on additional markets limited to US sports and selected
        bookmakers. Additional markets update at 5 minute intervals.
        Additional markets need to be accessed one event at a time using the
        /event/{eventId}/odds endpoint.

        Returns
        -------
        pd.DataFrame
            Dataframe of additional betting markets listed at
            https://the-odds-api.com/sports-odds-data/betting-markets.html#additional-markets
        """
        additional_markets_dict = {
            'market_key': ['alternate_spreads', 'alternate_totals', 'btts', 'draw_no_bet', 'h2h_3_way'],
            'market_name': ['Alternate Spreads (handicap)', 'Alternate Totals (Over/Under)',
                            'Both Teams to Score', 'Draw No Bet', 'Head to head / Moneyline 3 way'],
            'description': [
                'All available point spread outcomes for each team',
                'All available over/under outcomes',
                'Odds that both teams will score during the game. Outcomes are "Yes" or "No". Available for soccer.',
                'Odds for the match winner, excluding the draw outcome. A draw will result in a returned bet. Available for soccer',
                'Match winner including draw'
            ]
        }
        return pd.DataFrame(additional_markets_dict)

    @staticmethod
    def get_player_props(sport: str):
        """Get information on player props limited to US sports and selected US
        bookmakers, starting with FanDuel, DraftKings, Caesars, Bovada and more.
        Player props update at 5 minute intervals. Player props need to be accessed
        one event at a time using the /event/{eventId}/odds endpoint.

        Parameters
        ----------
        sport : str
            Sport key for which to return games and odds. Obtained from the
             /sports endpoint

        Returns
        -------
        pd.DataFrame
            Dataframe of player props listed at
            https://the-odds-api.com/sports-odds-data/betting-markets.html#player-props-api-markets
        """
        if sport == 'NFL':
            player_props_dict = {
                'market_key': [
                    'player_pass_tds',
                    'player_pass_yds',
                    'player_pass_completions',
                    'player_pass_attempts',
                    'player_pass_interceptions',
                    'player_pass_longest_completion',
                    'player_rush_yds',
                    'player_rush_attempts',
                    'player_rush_longest',
                    'player_receptions',
                    'player_reception_yds',
                    'player_reception_longest'
                ],
                'market_name': [
                    'Pass Touchdowns (Over/Under)',
                    'Pass Yards (Over/Under)',
                    'Pass Completions (Over/Under)',
                    'Pass Attempts (Over/Under)',
                    'Pass Intercepts (Over/Under)',
                    'Pass Longest Completion (Over/Under)',
                    'Rush Yards (Over/Under)',
                    'Rush Attempts (Over/Under)',
                    'Longest Rush (Over/Under)',
                    'Receptions (Over/Under)',
                    'Reception Yards (Over/Under)',
                    'Longest Reception (Over/Under)'
                ]
            }
        elif sport == 'NBA':
            market_key_arr = [
                'player_points'
                'player_rebounds',
                'player_assists',
                'player_threes',
                'player_double_double',
                'player_blocks',
                'player_steals',
                'player_turnovers'
            ]
            market_name_arr = [mk.split("_")[1].capitalize(
            ) + " (Over/Under)" for mk in market_key_arr]
            player_props_dict = {
                'market_key': market_key_arr,
                'market_name': market_name_arr
            }
        elif sport == 'NHL':
            market_key_arr = [
                'player_points'
            ]
        return pd.DataFrame(player_props_dict)
    import requests

    @staticmethod
    def _get_bookmakers_helper(region_index: int):
        """Helper function to get a list of bookmakers and their keys from the-odds-api.com website for a given region by index.

        Parameters
        ----------
        region_index : int
            Index of the region which reflects the ordering of regions on the website

        Returns
        -------
        bookmakers : list[dict]
            list of bookmakers and their keys for the a region
        """
        url = "https://the-odds-api.com/sports-odds-data/bookmaker-apis.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        bookmakers = []

        # Find the list of bookmakers
        bookmakers_section = soup.find_all('table')
        region_table = bookmakers_section[region_index]
        rows = region_table.find_all('tr')

        for row in rows:
            tds = row.find_all('td')
            d = dict()
            for i, td in enumerate(tds):
                if td.text.strip() != '':
                    if i == 0:
                        d['region'] = td.text.strip()
                    elif i == 1:
                        d['key'] = td.text.strip()
                    elif i == 2:
                        # Bookmaker name is the first element of the split list
                        d['title'] = td.text.strip().split('\n')[0]
            # Append the dictionary to the list of bookmakers if it is not empty
            if d != {}:
                bookmakers.append(d)
        return bookmakers

    @classmethod
    def get_bookmakers(cls, region: str = 'all'):
        """Get a list of bookmakers and their keys from the-odds-api.com website for a given region (or all regions if no region is specified).

        Parameters
        ----------
        region : str, optional
            region to get all bookmakers for, by default 'all', options are 'all', 'us', 'uk', 'au', 'eu'

        Returns
        -------
        bookmakers_all : list[dict]
            list of bookmakers and their keys for the given region
        """

        if region == 'all':
            for i in range(len(TheOddsAPI.BOOKMAKER_REGIONS)-1):
                bookmakers = TheOddsAPI._get_bookmakers_helper(i)
                if i == 0:
                    bookmakers_all = bookmakers
                else:
                    bookmakers_all.extend(bookmakers)
        else:
            if region not in TheOddsAPI.BOOKMAKER_REGIONS:
                raise ValueError(
                    f'Invalid region: {region}. Valid regions are: {TheOddsAPI.BOOKMAKER_REGIONS}')
            else:
                bookmaker_index = TheOddsAPI.BOOKMAKER_REGIONS.index(
                    region) - 1
                bookmakers_all = TheOddsAPI._get_bookmakers_helper(
                    bookmaker_index)
        return bookmakers_all
