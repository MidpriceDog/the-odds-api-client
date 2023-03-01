# the-odds-api-client
Python wrapper for The Odds API V4

## Getting Started

You can install the package using

```
pip install theoddsapi
```

Or you can run the following

```
git clone git@github.com:MidpriceDog/the-odds-api-client.git
```

and then 

```
make install
```

Either way, it is assumed you have Python 3, git, and pip installed.

## Example Usage

Instantiate an instance of `TheOddsAPI` by passing in an API key, which you 
should receive via email upon signing up for a subscription plan [here](!https://the-odds-api.com/).

```python
client = TheOddsAPI('YOUR_KEY_HERE')
```

Let's say you want to find out what the spread odds were on Fanduel's sportbook for games played on the 1st of January in the year 2023 around 12:00 UTC. Then, you would run the following:

```python
self._test_get_historical_odds(
            sport='basketball_nba',
            regions='us',
            markets='spreads',
            date='2023-01-01T12:00:00Z',
            bookmakers='fanduel',
            oddsFormat='american')
```


## Documentation

Please refer to the documentation[here](https://midpricedog.github.io/the-odds-api-client/#header-classes) for information on how to use this package. 

## Testing

Run

```
make test
```

<b>Note:</b> As a wrapper for The Odds API which requires the use of an API key,
testing this package requires using part of your the request quota associated
with the API key supplied. The usage quotas for running the tests suites
in the `test.py` file under the `tests` directory can be found in the schedule below. 

| Test Suite | Usage Quota |
| -------- | -------- |
| odds_suite | 3 |
| event_odds_suite | 2 |
| historical_odds_suite |  30 |
| usage_suite | 0 |
| scores_suite | 5 |
