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
logger.addHandler(logging.StreamHandler())

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


'''Opens 3 streams for desired tickers and determines arbitrage, if none is found
then the streams are closed and moved on to the next'''

'''works faster then the single socket'''

async def handle_stream(url, identifier, queue):
    try:
        with t.timeout(5):
            async with websockets.connect(url, timeout = 0.1, close_timeout=0.1)  as websocket1:
                message = await websocket1.recv()
                print(message) #-1121 BAD_SYMBOL
                if message == 0:
                    await websocket1.close()
                    print('connection failed')
                    raise Exception
                async for message in websocket1:
                    json_msg = json.loads(message)
                    json_msg = json_msg["data"]
                    pair = url[45:-11]
                    await queue.put((identifier,pair, json_msg,websocket1))
    except asyncio.TimeoutError: 
        await websocket1.close()
        queue.clear() # 
        print(f'timeout: {url[45:-11]}')
        print('prentast þetta?')   
    except asyncio.CancelledError:
        print('en þetta?')
        


async def calculate(queue):
    value_a = value_b = value_c = None
    profit = True
    while profit == True:
        identifier,pair, value,websocket1 = await queue.get()
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
                await websocket1.close()
                raise Exception
        

async def main():
    for tickers in tickerlist:
        queue = asyncio.Queue()
        try:
            await asyncio.gather(
                handle_stream(f'wss://stream.binance.com:9443/stream?streams={tickers[0].lower()}@bookTicker', "A", queue),
                handle_stream(f'wss://stream.binance.com:9443/stream?streams={tickers[1].lower()}@bookTicker', "B", queue),
                handle_stream(f'wss://stream.binance.com:9443/stream?streams={tickers[2].lower()}@bookTicker', "C", queue),
                calculate(queue),
            )
            '''Timeout ekki að virka '''

        except (Exception, asyncio.TimeoutError):
            for task in asyncio.gather():
                queue.clear()
                task.cancel()
        

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())