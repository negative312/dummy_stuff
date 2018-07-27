#!/usr/bin/env python

"""
    Connection details for Kraken
"""

import datetime
import json
import logging
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import requests

import _config as cfg

# Set up debug logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.package.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


def call_kraken_public_api(target_url, params=dict()):
    """
        Call the kraken public api and return a dictionary of the results
    """
    r = requests.get(cfg.public_base_url + target_url, params)
    json_data = json.loads(r.text)
    if json_data['error']:
        raise RuntimeError("Could not retrive {} asset pairs, exiting!".format(cfg.public_base_url + target_url))
    return json_data['result']
