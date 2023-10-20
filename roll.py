from ib_insync import *
import nest_asyncio
import pandas as pd
import pandas_ta as ta
import random
import datetime
import json
import math
from statistics import mean


def get_put_contracts(symbol):
    positions = ib.positions()
    put_strike = 0
    for position in positions:
        if position.contract.symbol == symbol:
            print(symbol + " : strike " + str(position.contract.strike))
            put_strike = position.contract.strike
            print(position)
            print(position.contract.symbol)
            print(position.contract.secType)
            print(position.contract.conId)
            chains = ib.reqSecDefOptParams(position.contract.symbol, '', 'STK', position.contract.conId)
            chain = next(c for c in chains if c.exchange == 'SMART')
            strikes = [strike for strike in chain.strikes
                       if strike == put_strike]
            expirations = sorted(exp for exp in chain.expirations)[:3]
            # rights = ['P', 'C']
            rights = ['P']
            contracts = [Option(symbol, expiration, strike, right, 'SMART', tradingClass=symbol)
                         for right in rights
                         for expiration in expirations
                         for strike in strikes]
            # print(contracts)
            return contracts


def on_pending_tickers(tickers):
    positions = ib.positions()
    for t in tickers:
        symbol = t.contract.symbol
        put_strike = 0
        for position in positions:
            if position.contract.symbol == symbol:
                print(symbol)
                print(position.contract.strike)
                put_strike = position.contract.strike
                print(t.contract.symbol)
                print(t.contract.secType)
                print(t.contract.conId)
                chains = ib.reqSecDefOptParams(t.contract.symbol, '', t.contract.secType, t.contract.conId)
                chain = next(c for c in chains if c.exchange == 'SMART')
                print(chain)
                strikes = [strike for strike in chain.strikes
                           if strike == put_strike]
                print(strikes)
                expirations = sorted(exp for exp in chain.expirations)[:3]
                # rights = ['P', 'C']
                rights = ['P']
                contracts = [Option(symbol, expiration, strike, right, 'SMART', tradingClass=symbol)
                             for right in rights
                             for expiration in expirations
                             for strike in strikes]
                # print(contracts)
                return contracts

        # print(symbol)
        # print(t.marketPrice())
        # chains = ib.reqSecDefOptParams(t.contract.symbol, '', t.contract.secType, t.contract.conId)
        # print(util.df(chains).head(10))
        # chain = next(c for c in chains if c.exchange == 'SMART')


ib = IB()
ib.connect('127.0.0.1', 7497, clientId=12)
nest_asyncio.apply()  # patch for asyncio to stop a loop error when trying to ib.sleep
account = 'DU4792662'  # paper money

# symbols = ["TSLA", "NVDA", "AAPL", "MSFT", "AMD", "AMZN", "META", "GOOGL", "NFLX"]
symbols = ["AFL"]

contracts = [Stock(symbol, 'SMART', 'USD') for symbol in symbols]
ib.qualifyContracts(*contracts)

#  subscribe to market data
for contract in contracts:
    ib.reqMktData(contract, '233', False, False)
    print(contract.symbol + " connected")

#  get the tickers
# tickers = ib.reqTickers(*contracts)
#
# #  create an event handler for when the ticker updates
# # ib.pendingTickersEvent += on_pending_tickers
# ib.sleep(10)
# on_pending_tickers(tickers)

put_contracts = get_put_contracts("AFL")
print(put_contracts)
