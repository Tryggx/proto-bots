from GetPairs import GetPairs
from GetTickerPrices import GetTickerPrices

class Compare:
    def __init__(self):
        self.getpairs = GetPairs()
        self.getprices = GetTickerPrices()
        self.pairs = None
        self.pair1 = "XVG","USDT" 
        self.pair2 = "XVG","BTC"
        self.pair3 = "BTC","USDT" 
        self.info = []


    def get_pairs(self):
        self.pairs = self.getpairs.find()


    def Pair_info(self):
        self.info.append(GetTickerPrices.getprice(self,self.pair1))
        self.info.append(GetTickerPrices.getprice(self,self.pair2))
        self.info.append(GetTickerPrices.getprice(self,self.pair3))
        return self.info
    
    def possible_profit(self,info):
        """Want left = 1/Ask, Want right = Bid"""
        #fyrir forward test viljum við vinstri, vinstri, hægri.
        # reverse er akkurat öfugt
        arb_forw = ((1/float(info[0]["lowestAsk"])*float(info[1]["highestBid"])*float(info[2]["highestBid"]))-1)*100
        arb_rev = ((1/float(info[2]["lowestAsk"])*1/float(info[1]["lowestAsk"])*float(info[0]["highestBid"]))-1)*100
        return arb_forw,arb_rev



        


# Usdt/eth --> Eth/WOO ---> WOO/Usdt
if __name__ == "__main__":
    pairs = Compare()
    info = pairs.Pair_info()
    print(pairs.possible_profit(info))