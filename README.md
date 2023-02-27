# the-odds-api-client
Python wrapper for The Odds API V4

## Getting Started

Run

```
pip install -r requirements.txt
```

## Example Usage

Instantiate an instance of `theOddsAPI` by passing in an API key, which you 
should receive via email upon signing up for a subscription plan [here](!https://the-odds-api.com/).

```python
client = theOddsAPI('YOUR_KEY_HERE')
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

You can find the documentation for the Odds API Client hosted [here](https://midpricedog.github.io/the-odds-api-client/#header-classes).

## Testing

A test of this package can be done by running the following command

```
python tests/test.py
```

<b>Note:</b> As a wrapper for The Odds API which requires the use of an API key,
testing this package requires using part of your the request quota associated
with the API key supplied. The usage quota for running the various tests suites
in `tests.py` can be found in the schedule below. 

| Test Suite | Usage Quota |
| -------- | -------- |
| odds_suite | 3 |
| event_odds_suite | 2 |
| historical_odds_suite |  30 |
| usage_suite | 0 |
| scores_suite | 5 |
