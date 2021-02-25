![](https://media.giphy.com/media/v18xOnxDRt8aI/giphy.gif)

# Algo Trading

A live trading and backtesting python app.

## Requirements

* [Python](https://www.python.org/) 3.9.1
* [pyenv](https://github.com/pyenv/pyenv)
* [MongoDB](http://www.mongodb.org/) 3.2
* [talib prerequisites](https://mrjbq7.github.io/ta-lib/install.html)

## Installation

### MacOS: 

pyenv installation and python version:
```
brew update
brew install pyenv
pyenv install 3.9.2
```

install ta-lib:
```
brew install ta-lib
```

install python dependencies and clone repo
```sh
git clone https://github.com/joshfermin/algo-trading.git
cd algo-trading
pyenv local 3.9.1
pip install -e .
```

## Usage
### Setup
- Make a copy of the `.env.example` file and rename it to `.env`, fill in your robinhood data there

### Backtesting
- Edit or copy paste the example config under `./algo-trading/configs` with your strategies, if no config provided will default to the example config.
```
python ./tests/backtest_our_fate.py --config=<name of config here>
```

### Live Trading
```
python ./algo_trading/live_trading.py --config=<name of config here>
```

### Data Collection
- Use the `okcoin.py` script to gather market data from the [OKCoin Spot Price API](https://www.okcoin.com/about/rest_api.do) at the interval of minute, hour and day for ETH, LTC and BTC.
- If you wish to use any data collection you must have mongodb connection string setup in your .env
```sh
$ python ./algo-trading/data_collection/okcoin.py
```
