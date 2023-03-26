import pandas
import numpy
import os

NOF_TRADING_DAYS = 252

metadata = pandas.read_csv("symbols_meta.csv")
screener = pandas.read_csv("nasdaq_screener.csv")
stocks_dir = os.path.join(os.getcwd(), "stocks")
dir_list = os.listdir(stocks_dir)
nasdaq_symbols = []


stocks = {}
for file in dir_list[:2000]:
    symbol = file.strip(".csv")
    nasdaq_symbols.append(symbol)
    stocks[symbol] = pandas.read_csv(f"stocks/{file}")
    stocks[symbol]['TimeStamp'] = pandas.to_datetime(stocks[symbol]['Date'],format= '%Y-%m-%d')
    stocks[symbol].drop(columns=['Date'],inplace=True)


def get_period(start, end):
    valid = {}  # stocks which were active during selected period
    nof_days = {}  # frequency of the number of records 

    for sym in nasdaq_symbols:
        start_date = stocks[sym]['TimeStamp'].min()
        end_date = stocks[sym]['TimeStamp'].max()

        if start_date <= start and end_date >= end:
            trimmed = stocks[sym][(stocks[sym]['TimeStamp'] >= start) & (stocks[sym]['TimeStamp'] <= end)]
            valid[sym] = trimmed
            recs = len(valid[sym])

            if recs in nof_days: nof_days[recs] += 1
            else: nof_days[recs] = 0

    # remove stocks which have missing data
    desired_nof_records = max(nof_days, key=nof_days.get)
    valid = {k:v for k, v in valid.items() if len(v) == desired_nof_records}
    return valid


def symbol_sector_map(symbols):
    mapping = {}
    for sym in symbols:
        sector = screener[screener['Symbol'] == sym]['Sector'].iloc[0]
        mapping[sym] = sector
    return mapping

