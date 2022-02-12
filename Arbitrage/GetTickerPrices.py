from GetPairs import GetPairs
import json
import requests

class GetTickerPrices:
    def __init__(self):
        self.pair_url = None
        self.data = None
        self.pair_dict = {}

    def getprice(self,pair): # Skoða að breyta í websockets
    #    pair = pair.split(",")
        self.pair_url = f"https://data.gateapi.io/api2/1/ticker/{pair[0].lower()}_{pair[1].lower()}"
        self.data = requests.get(self.pair_url).json()
        return self.data


if __name__ == "__main__":
    pairs = GetPairs()
    samepairs = pairs.find(pairs)
    pairs.save(samepairs)
