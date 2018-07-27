#!/usr/bin/env python

"""
    Create plotting and data for daily spreads which may be useful for
    our market making strategy
"""

import argparse
import csv
import datetime
import json
import logging
import numpy as np
import pandas as pd

import _config as cfg
import kraken_connection as kc

logging.basicConfig(level=logging.INFO)

def val_transform(key, val, tmp):
    """
        Make the csv output a bit prettier
    """
    if isinstance(val, list):
        for item, value in zip(cfg.ticker_dict[key], val):
            tmp[item] = value
    else:
        tmp[cfg.ticker_dict[key]] = val

def dump_to_csv(dic):
    """
        As stated in the title...
    """
    instrument_array = dic.values()
    for key, value in dic.items():
        dic[key]["s"] = key 

    rows = list(dic.values())

    # Manipulate values here for csv dump (https://www.kraken.com/help/api)
    final_vals = []
    for row in rows:
        tmp = {}
        for key, value in row.items():
            val_transform(key, value, tmp)
        final_vals.append(tmp)

    df = pd.DataFrame(final_vals).set_index("symbol")
    df.to_csv("logs/tickers_{}.csv".format(datetime.datetime.now().strftime("%Y%m%d_%H%m%S")))
    
def process():
    # Get today's tradeable pairs
    instruments = kc.call_kraken_public_api(cfg.target_urls["asset_pairs"])
    instruments = list(instruments.keys())
    values = kc.call_kraken_public_api(cfg.target_urls["ticker_info"],
            params={"pair": ",".join(instruments)})
    dump_to_csv(values)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pushes all ticker information to csvs")
    parser.add_argument("--verbose", dest="v", action="store_true", default=False)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO) 
    logger = logging.getLogger(__name__)
    
    process()
