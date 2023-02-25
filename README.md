# the-odds-api-client
Python wrapper for The Odds API V4

## Getting Started

Run

```
pip install -r requirements.txt
```

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
