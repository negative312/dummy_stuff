"""
    Config file for kraken API details, essentially stores the log file and
    connection details
"""

public_base_url = "https://api.kraken.com/0/public"
private_base_url = "https://api.kraken.com/0/private"

target_urls = {
    "server_time": "/Time",
    "assets": "/Assets",
    "asset_pairs": "/AssetPairs",
    "depth": "/Depth",
    "ohlc": "/OHLC",
    "spread": "/Spread",
    "ticker_info": "/Ticker"
}

ticker_dict = {
        "s": "symbol",
        "a": ["ask_price", "ask_whole_lot_volume", "ask_lot_volume"],
        "b": ["bid_price", "bid_whole_lot_volume", "bid_lot_volume"],
        "c": ["last_trade_price", "last_trade_lot_volume"],
        "v": ["volume_today", "volume_last_24_hours"],
        "p": ["volume_weight_averaged_price_today",
              "volume_weight_averaged_price_24_hours"],
        "t": ["number_of_trades_today", "number_of_trades_24_hours"],
        "l": ["low_today", "low_24_hours"],
        "h": ["high_today", "high_24_hours"],
        "o": "todays_opening_price"
}
