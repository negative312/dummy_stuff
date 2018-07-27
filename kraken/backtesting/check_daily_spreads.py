#!/usr/bin/env python
"""
    Create plotting and data for daily spreads which may be useful for
    our market making strategy
"""

import argparse
import datetime
import json
import logging
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import pandas as pd

import _config as cfg
import kraken_connection as kc


logging.basicConfig(level=logging.INFO)

def generate_plot(vals):
    d = pd.DataFrame(vals, columns=["times", "bids", "offers"])
    d.set_index(keys="times", inplace=True)
    d = d.astype(float)
    ax = d.plot(xticks=d.index)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    plt.show()

def calculate_potential_fills(vals):
    """
        Input:  A dataframe containing a timestamp, bid and ask
        Output: Calculates the nubmer of times the ask (and bid) crosses a prior
                NBBO
    """
    df = pd.DataFrame(vals, columns=["times", "bids", "offers"])
    bid_map = set()
    ask_map = set()
    stats = []
    for index, row in df.iterrows():
        if row["bids"] in ask_map:
            stats.append("Bid crossed a previous ask nbbo. Spread opportunity {}:{}".format(row["bids"], row["times"]))
            ask_map.discard(row["bids"])
        if row["offers"] in bid_map:
            stats.append("Offer crossed a previous bid nbbo. Spread opportunity {}:{}".format(row["offers"], row["times"]))
            bid_map.discard(row["bids"])

        bid_map.add(row["bids"])
        ask_map.add(row["offers"])

    for row in stats:
        print(row)

def process(symbol, plot):
    # Get today's tradeable pairs
    instruments = kc.call_kraken_public_api(cfg.target_urls["asset_pairs"])
    
    if symbol not in list(instruments.keys()):
        raise RuntimeError("{} not in todays tradeable pairs, cannot retrieve info!".format(symbol))

    results = kc.call_kraken_public_api(cfg.target_urls["spread"],
                params={"pair": ",".join([symbol])})
    vals = results[symbol]
    vals = [[datetime.datetime.fromtimestamp(date), x, y] for date, x, y in vals]

    if plot:
        generate_plot(vals)
    else:
        calculate_potential_fills(vals)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takes a symbol and creates a graph of daily spread data")
    parser.add_argument("--symbol", dest="symbol", required=True)
    parser.add_argument("--verbose", dest="v", action="store_true", default=False)
    parser.add_argument("--plot", dest="plot", action="store_true", default=False)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO) 
    logger = logging.getLogger(__name__)
    
    if args.v:
        logger.debug("Running with verbose logging!")

    process(args.symbol, args.plot)
