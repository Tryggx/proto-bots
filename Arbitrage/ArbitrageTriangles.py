from binance.client import Client
import config
import json
import collections
from operator import itemgetter
PRIMARY = ['ETH', 'USDT', 'BTC', 'BNB', 'ADA', 'SOL', 'LINK', 'LTC', 'UNI', 'XTZ']
ticker1 = None
ticker2 = None
ticker3 = None

def get_prices():
    client = Client(config.binance_api_key, config.binance_api_secret)
    prices = client.get_orderbook_tickers()
    prepared = collections.defaultdict(list)
    for ticker in prices:
            pair = ticker['symbol']
            for primary in PRIMARY:
                if pair.endswith(primary):
                    secondary = pair[:-len(primary)]
                    prepared[primary].append([pair])
                    prepared[secondary].append([pair])
    return prepared

def get_tickers(prices):
    triangles = collections.defaultdict(dict)
    starting_coin = 'USDT'
    Pair = 'BTCUSDT'
    for triangle in recurse_triangle(prices, starting_coin, starting_coin,Pair):
        if triangle[starting_coin][0] != triangle[starting_coin][2]: #koma í veg fyrir duplicates í lokinn
            sec = triangle[starting_coin][1]
            thi = triangle[starting_coin][2]
            if not sec.startswith(thi[:-len(starting_coin)]):
                if starting_coin not in triangles:
                    for key,values in triangle.items():
                        triangles[key] = [values]
                else:
                    for key,values in triangle.items():
                        triangles[key].append(values)
    return triangles


def recurse_triangle(pairs, current_coin, starting_coin,currentpair, depth_left=3): 
    if depth_left > 0:
        coinpairs = pairs[current_coin]
        for pair in coinpairs:
            if isinstance(pair,list):
                secondary = pair[0][:-len(current_coin)]
                currentpair = pair[0]
            else:
                secondary = pair[:-len(current_coin)]
                currentpair = pair
            coin = secondary
            for triangle in recurse_triangle(pairs, coin, starting_coin,currentpair, depth_left - 1):
                triangle[starting_coin].append(currentpair)
                yield triangle
    elif currentpair.endswith(starting_coin):
        yield {starting_coin:[]}
        


    

filepath = "symboltriangles.json"
#prepared = 
prices = get_prices()
triangles = get_tickers(prices)

with open(filepath, 'w', encoding = 'utf-8') as outfile:
    json.dump(triangles, outfile, indent = 4, ensure_ascii = False)