
import requests
import json
import os
from itertools import combinations


class GetPairs:
    def __init__(self):
        self.filepath = os.path.dirname(os.path.dirname(__file__)) + '/Arbitrage/eth_usdt.json'
        self.pair_url = None
        self.data = None
        self.pair_dict = {}
    
    def checkdata(self):
        try:
            with open(self.filepath,'r') as f: #opnar json file frá directory
                self.data = json.loads(f.read()) 
            self.pair_dict = self.data
            return self.pair_dict
        except os.error:
            self.pair_url = "https://data.gateapi.io/api2/1/pairs"
            self.data = requests.get(self.pair_url).json()
        return self.data


#    def find(self,pairs):
#        if pairs.data == None:
#            pairs = GetPairs.checkdata(self)
#        else: 
#            pass
#        if isinstance(pairs,list):
#            for i in pairs:
#                ticker = i.split("_")
#                if ticker[1] in self.pair_dict:
#                    self.pair_dict[ticker[1]].append(ticker[0])
#                else:
#                    self.pair_dict[ticker[1]] = [ticker[0]]
#            GetPairs.save(self,self.pair_dict)
#            return self.pair_dict
#        else:
#            return self.pair_dict
 
    def find2(self,pairs): 
        ticker_list = ["ETH","USDT","BTC"] # græja lista sem ber saman við usdt pairs file, þannig hægt að sja hvað er bæði usdt og eth/btc
        single_list = []
        double_list = []
        triple_list = []
        for i in pairs: 
            k = i.split("_")
            if k[1] in ticker_list:
                single_list.append(k[0])
        for i in single_list:
            occurrences = single_list.count(i)
            if occurrences == 3 and i not in triple_list:
                triple_list.append(i)
        #    if k[0] not in single_list and k[1] in ticker_list: #in ticker_list: # finnur coins sem deila ETH, BTC og USDT pari
        #        single_list.append(k[0])
        #    elif k[0] in single_list and k[1] in ticker_list:
        #        double_list.append(k[0])
        #    elif k[0] in single_list and double_list and k[1] in ticker_list:
        #        triple_list.append(k[0])
        return triple_list



    #    pairs = list(combinations(pairs,3))
    #    return pairs
    
    def save(self,pairs):
         with open(self.filepath,'w',encoding='utf-8') as outfile:
            json.dump(pairs ,outfile, indent=4)

    


if __name__ == "__main__":
    pairs = GetPairs()
    getpairs = pairs.checkdata()
    samepairs = pairs.find2(getpairs)
    #pairs.save(samepairs)
    print(samepairs)