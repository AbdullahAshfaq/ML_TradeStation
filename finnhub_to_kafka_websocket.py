
from time import gmtime, strftime
import uuid
import json
import websocket
from credentials import *
from utils.mysql_utils import MySQL_Class

# Kafka libraries
from kafka import KafkaProducer
from kafka.errors import KafkaError


# Kafka Producer: Send messages to Kafka topics
producer = KafkaProducer(
    value_serializer=lambda v: json.dumps(v).encode('utf-8'), 
    bootstrap_servers='0.0.0.0:9092,0.0.0.0:9093,0.0.0.0:9094'
    )

mysql_connection = MySQL_Class(  
    host="localhost",
    user="root",
    password="example",
    database="finnhub"
    )

# This function is called whenever a message is received
def on_message(ws, message):
    print(message)
    # Message is in str and can be converted to json using json.loads
    stocks_dict = json.loads(message)

    try:
        if stocks_dict is not None and "data" in stocks_dict:
            for stockitem in stocks_dict['data']:
                try:
                    if stockitem is not None and stockitem['s'] is not None: 
                        print(stockitem['p'])
                        uuid_key = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())
                        if ( stockitem['s'] != '' ):
                            if ':' in stockitem['s']:
                                stock_symbol = stockitem['s'].split(':')[-1]
                            else:
                                stock_symbol = stockitem['s'] 
                            # Symbol name is kafka topic name
                            kafka_value = {
                                'uuid': uuid_key, 
                                'ts': float(stockitem['t']), 
                                'currentts': float(strftime("%Y%m%d%H%M%S",gmtime())), 
                                'volume': float(stockitem['v']),
                                'price': float(stockitem['p']) 
                                }
                            producer.send(stock_symbol, kafka_value)
                            producer.flush()
                            
                            # Write to MySQL
                            insert_statement = "INSERT INTO "+ stock_symbol +" (uuid, ts, currentts, volume, price) VALUES (%s, %s,%s, %s,%s)"
                            mysql_connection.insert(insert_stmt=insert_statement, values=tuple(kafka_value.values()))

                except NameError:
                    print("skip it")
    except Exception as ex:
        print(ex)



def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}') # BTCUSDT is always running. Others run only when market is open
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')




if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={API_KEY}",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()