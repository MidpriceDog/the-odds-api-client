Module api
==========

Classes
-------

`theOddsAPI(api_key: str)`
:   

### Class variables

`HOST`
:

### Static methods

`get_additional_markets()`
:   Get information on additional markets limited to US sports and selected
    bookmakers. Additional markets update at 5 minute intervals.
    Additional markets need to be accessed one event at a time using the
    /event/{eventId}/odds endpoint.
    
    Returns
    -------
    pd.DataFrame
        Dataframe of additional betting markets listed at
        https://the-odds-api.com/sports-odds-data/betting-markets.html#additional-markets

`get_featured_betting_markets()`
:   Get the most common markets that are featured by bookmakers.
    Terminology for betting markets can vary by country, sport and even
    amongst bookmakers.
    
    Returns
    -------
    pd.DataFrame
        Dataframe of featured betting markets listed at
            https://the-odds-api.com/sports-odds-data/betting-markets.html

`get_player_props(sport: str)`
:   Get information on player props limited to US sports and selected US
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

### Methods

`get_event_odds(self, **kwargs)`
:   Returns odds for a single game. Accepts any available betting markets
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
    bookmakers : list[int]
        The bookmaker(s) to be returned. Every group of 10 bookmakers
        counts as 1 request.

`get_historical_odds(self, **kwargs)`
:   Returns a snapshot of games with bookmaker odds for a given sport, region
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
    eventId : list[str]
        Comma-separated game id(s) of upcoming or live game(s). Filters the
        response to only return games for the specified game ids, provided
        those games have not expired.
    bookmakers : list[int]
        The bookmaker(s) to be returned. Every group of 10 bookmakers
        counts as 1 request.

`get_odds(self, **kwargs)`
:   Returns a list of upcoming and live games with recent odds for a
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
    bookmakers : list[int]
        The bookmaker(s) to be returned. Every group of 10 bookmakers
        counts as 1 request.

`get_requests_remaining(self)`
:   Get the number of requests remaining for current month
    
    Returns
    -------
    int
        Number of requests remaining for current month

`get_requests_used(self)`
:   Get the number of requests used in current month
    
    Returns
    -------
    int
        Number of requests used in current month

`get_scores(self, **kwargs)`
:   Returns a list of upcoming, live and recently completed games for a
    given sport. Live and recently completed games contain scores. Games
    from up to 3 days ago can be returned using the daysFrom parameter.
    Live scores update approximately every 30 seconds.
    
    Parameters
    ----------
    sport : str
        Sport key for which to return games and odds. See list of covered
            sports at https://the-odds-api.com/sports-odds-data/sports-apis.html
    params : dict
        See https://the-odds-api.com/liveapi/guides/v4/#parameters-3

`get_sports(self, params)`
: