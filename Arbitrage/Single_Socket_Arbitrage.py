import websockets
import json
import asyncio
import config 
from binance.client import Client
from concurrent.futures.thread import ThreadPoolExecutor
import logging
import async_timeout as t
from time import time
import datetime


logger = logging.getLogger('asyncio')
logger.setLevel(logging.WARNING)
#logger.addHandler(logging.StreamHandler())

tickerlist = []
f = open("symboltriangles.json")
triangles = json.load(f)
for key,value in triangles.items():
    for i in value:
     tickerlist.append(i)

#PRIMARY = ['ETH', 'USDT', 'BTC', 'BNB', 'ADA', 'SOL', 'LINK', 'LTC', 'UNI', 'XTZ']
#ticker1 =  "FUNUSDT"
#ticker2 =  "FUNBTC"
#ticker3 =  "BTCUSDT"

#from concurrent.futures import TimeoutError as ConnectionTimeoutError


'''Leitar að arbitrage með constant stream og iterate-ar í gegnum lista þar til rétt par í stream finnst'''
'''Reiknar svo arbitrage'''



async def handle_stream(ticker,queue,identifier):
        async with websockets.connect('wss://stream.binance.com:9443/ws/!bookTicker') as websocket1:
            while True:
                message = await websocket1.recv()
                #async for ticker in tickerlist:
                json_msg = json.loads(message)
                    #if websockets.recv() == websockets.pong():
                    #    await websocket1.close()
                    #    raise Exception
                if json_msg['s'] == ticker:
                    await asyncio.sleep(1)
                    await queue.put((json_msg,identifier,ticker))
                


async def calculate(queue):
    value_a = value_b = value_c = None
    profit = True
    while profit == True:
        value,identifier,pair= await queue.get()
        if identifier == 'A':
            value_a = value["b"],value['a']
            pair_a = pair
        elif identifier == 'B':
            value_b = value["b"],value['a']
            pair_b = pair
        else: 
            value_c = value["b"],value['a']
            pair_c = pair
        if value_a is not None and value_b is not None and value_c is not None:
            """Want left = 1/Ask, Want right = Bid"""
            arb_forw = ((1/float(value_a[1])*float(value_b[0])*float(value_c[0]))-1)*100
            arb_rev = ((1/float(value_c[1])*(1/float(value_b[1]))*float(value_a[0]))-1)*100
            if arb_forw > 0.05 or arb_rev > 0.05: #Græja round á profit og prenta hvaða par er í gangi.
                print(f'profit :{round(arb_forw,4)}, {round(arb_rev,4)} ---> {pair_a}/{pair_b}/{pair_c} \n \n {datetime.datetime.now()}')
                
            else: 
                print(f'{pair_a}/{pair_b}/{pair_c} NO PROFIT \n {round(arb_forw,4)}, {round(arb_rev,4)}\n {datetime.datetime.now()} \n ')
                profit = False
                raise Exception
        
        '''Eftir að implementa tímamælingu'''
        '''fara yfir hvort þetta sé að gera þetta concurrently, virkar eins og eigi að gerast hraðar'''

'''Staðfesta að stream sé ekki að lokast, myndi hægja á þessu.'''

async def main():
    for tickers in tickerlist:
        queue = asyncio.Queue()
        try:
            async with t.timeout(10):
                await asyncio.gather(
                    handle_stream(tickers[0],queue,'A'),
                    handle_stream(tickers[1],queue,'B'),
                    handle_stream(tickers[2],queue,'C'),
                    calculate(queue))
        #    wsapp.run_forever()
        except (Exception, asyncio.TimeoutError):
            for task in asyncio.gather():
                queue.clear()
                task.cancel()
        

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())