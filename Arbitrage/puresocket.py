import websocket, json,logging
url = 'wss://stream.binance.com:9443/stream?streams=funusdt@bookTicker'

def on_message(ws,message):
    print(message)

def on_close(ws):
    print('Closed')

def on_error(ws,error):
    print(error)

ws = websocket.WebSocketApp(url, on_message=on_message, on_close=on_close, on_error=on_error)
ws.run_forever()
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('websocket')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
