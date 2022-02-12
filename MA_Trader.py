#import Binance_data
import websocket, json, pprint, talib, numpy
import matplotlib.pyplot as plt
import pandas as pd

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_5m"
"https://github.com/man-c/pycoingecko"
RSI_PERIOD = 2
RSI_OVERBOUGHT = 65
RSI_OVERSOLD = 35

TRADE_SYMBOL = "ETHUSD"
TRADE_QUANTITY = "0.05"

closes = []
#
""" Eftirfarandi er ef farið er live """
#def on_open(ws):
#    print("opened connection")
#
#def on_close(ws):
#    print('closed connection')
#
#def on_message(ws, message):
#    global closes 
#    print("received message")
#    json_message = json.loads(message) #loadar skilaboði frá binance
#    pprint.pprint(json_message) #prentar fínpússað data með pprint
#
#    candle = json_message["k"] # tekur gögn frá kerti og kallar það candle
#    is_candle_closed = candle["x"] # sækir hvort kertið sé lokað (TRUE/FALSE)
#    close = candle["c"] #Sækir verðið 
"""L"""

def data_read(filename):
    df = pd.read_csv(filename, delimiter=',')
    #df = df.iloc[-1000:,] # ef skjalið er stórt og þarf að minnka datasettið
    data = df["close"]
    data.reset_index(drop=True, inplace=True) #núllar indexið
    time = df["timestamp"]
    time.reset_index(drop=True, inplace=True) #núllar indexið
    print(data)
    print(time)
    return data,time

          

def backtester_rsi(data,cash):
    x_value = []
    y_value = []
    x2_value = []
    x3_value = []
    buy = []
    sell = []
    #is_candle_closed = 
    closes = []
    in_position = False
    tokens = 0
    profit = 0
    buy_price = 0

    for place, data_set in enumerate(data):
        closes.append(data_set)
        np_closes = numpy.array(closes)
    #    ma1 = talib.MA(np_closes,timeperiod=10, matype=0)
    #    ma2 = talib.MA(np_closes,timeperiod=20, matype=0)
        ma1 = talib.EMA(np_closes,timeperiod=10)
        ma2 = talib.EMA(np_closes,timeperiod=20)

        last_price = closes[-1]
        if ma1[place]>ma2[place]:
            if in_position:
                pass
    
            else:
                tokens = (cash/2)/last_price
                buy_price = last_price
                cash -=(cash/2)
                in_position = True
                x3_value.append(time[place])
                buy.append(last_price)
                print(f"bought at: {last_price}")
        if ma2[place]>ma1[place]:
            if in_position:
                profit += (tokens*(last_price))-cash
                cash += (last_price*tokens)
                print(f"Sold at: {last_price}")
                print(f"P: {profit} : {last_price} : C {cash}")
                in_position = False
                tokens = 0
                x2_value.append(time[place])
                sell.append(last_price)
            else: 
                pass
        #x_value.append(time[place]) #portfolio value
        #y_value.append(cash)
        x_value.append(time[place])
        y_value.append(ma1[place])
    #plot_graph(x_value,y_value)
    plt.plot(x_value, ma1, color='blue')
    plt.plot(x_value, ma2, color='red')
    plt.plot(x_value,np_closes)
    plt.plot(x2_value, sell, "o" ,color='red' )
    plt.plot(x3_value,buy, "x",color='green')
    plt.show()
    return cash,profit



   
    #    if len(closes) > RSI_PERIOD: #Reiknar RSI (ef lengd er stærri en period)
    #        np_closes = numpy.array(closes) #breytir úr lista í numpy array
    #        ma1 = talib.MA(np_closes, RSI_PERIOD) #kallar í innbyggt rsi function í talib
    #        #print("all rsis calculated so far")
    ##        print(rsi)
    #        last_ma1 = rsi[-1]
    #        last_price = closes[-1]
    #        #print(f"the current rsi is {last_rsi}")
    #        if last_rsi > RSI_OVERBOUGHT:
    #            if in_position:
    #                #if last_price-buy_price:
    #                profit += (tokens*last_price)-cash
    #                cash += (tokens*last_price)
    #                print(f"P:{profit}, {last_price}, C{cash}")
    #                tokens = 0
    #                in_position = False
    #            else: 
    #                pass
    #        if last_rsi < RSI_OVERSOLD:
    #            if in_position:
    #                pass
    #            else:
    #                tokens += (cash/2)/last_price
    #                cash -= (cash/2)
    #                in_position = True
    #                buy_price = last_price
    #                print(f"T:{tokens},{last_price}, {cash}")
    #    x_value.append(time[place])
    #    y_value.append(cash)
#    plot_graph(time,ma1)
#    plot_graph(time,ma2)
#    plt.show()
#    return cash,profit


def plot_graph(x, y):
    """
    Plots our Graph
    """
    plt.plot(x, y)
    plt.xlabel("Minute")
    plt.ylabel("Portfolio Value")
    
   
    

"""main"""
filename = "ADAUSDT-1d-data.csv"
data,time = data_read(filename)
cash = 1000
cash_back,profit = backtester_rsi(data,cash)
print(f"{cash_back},{profit}")



#ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
#ws.run_forever()