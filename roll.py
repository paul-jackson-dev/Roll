from ib_insync import *
import nest_asyncio
import pandas as pd
import pandas_ta as ta
import random
import datetime
import json
import math
from statistics import mean


def on_pending_tickers(tickers):
    for t in tickers:
        symbol = t.contract.symbol
        print(symbol)


ib = IB()
ib.connect('127.0.0.1', 7497, clientId=12)
nest_asyncio.apply()  # patch for asyncio to stop a loop error when trying to ib.sleep
account = 'DU4792662'  # paper money

# symbols = ["TSLA", "NVDA", "AAPL", "MSFT", "AMD", "AMZN", "META", "GOOGL", "NFLX"]
symbols = ["AAPL", "MSFT"]

contracts = [Stock(symbol, 'SMART', 'USD') for symbol in symbols]
ib.qualifyContracts(*contracts)

#  subscribe to market data
for contract in contracts:
    ib.reqMktData(contract, '233', False, False)
    print(contract.symbol + " connected")

#  get the tickers
tickers = ib.reqTickers(*contracts)

#  create an event handler for when the ticker updates
ib.pendingTickersEvent += on_pending_tickers
