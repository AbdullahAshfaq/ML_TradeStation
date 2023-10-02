'''
Purpose:
Read News, stock fundamentals, 1 min candles in batches
'''

import finnhub
from datetime import datetime, timedelta

from utils.mysql_utils import MySQL_Class
from credentials import *


def get_stock_news(SYMBL):
    '''
    Company News API
    Method: Get
    
    '''

    finnhub_client = finnhub.Client(api_key=API_KEY)

    # News in 1 Hr
    to_date = datetime.today().strftime('%Y-%m-%d')
    from_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    news_lst = finnhub_client.company_news(SYMBL, _from=from_date, to=to_date)
    if len(news_lst)<=0:
        print(f"No News found for {SYMBL}")
        return
    

    values = []
    for n in news_lst:

        val = tuple([n.get('datetime',0),
        n.get('source','not_found'),
        n.get('headline','not_found'),
        n.get('summary','not_found')])
        
        values.append(val)

    # Inserting into MySQL
    mysql_connection = MySQL_Class(  
        host="localhost",
        user="root",
        password="example",
        database="finnhub"
        )
    
    insert_statement = "REPLACE INTO "+ SYMBL +"_news (datetime, source, headline, summary) VALUES (%s, %s,%s, %s)"
    mysql_connection.insert(insert_stmt=insert_statement, values=values)


def get_candle_5min(SYMBL):
    '''
    SYMBL: AAPL
    timeframe: '1','5','60','D','W'
    '''
    finnhub_client = finnhub.Client(api_key=API_KEY)

    to_datetime = datetime.now()
    from_datetime = datetime.now() - timedelta(minutes=5)

    from_datetime = int(from_datetime.timestamp())
    to_datetime = int(to_datetime.timestamp())

    candle_data = finnhub_client.stock_candles(SYMBL, '5', from_datetime, to_datetime)

    values = []
    if candle_data.get('s','no_data') == 'ok' and candle_data.get('c') is not None: # If some data returned in candles
        for i in range(len(candle_data['c'])):
            val = tuple([candle_data['t'][i], candle_data['v'][i], candle_data['c'][i], candle_data['h'][i], candle_data['l'][i], candle_data['o'][i]])
            values.append(val)
    else:
        print("No data received from Finnhub")
        return
    # Inserting to MySQL
    mysql_connection = MySQL_Class(  
        host="localhost",
        user="root",
        password="example",
        database="finnhub"
        )
    
    if ':' in SYMBL:
        stock_symbol = SYMBL.split(':')[-1]
    else:
        stock_symbol = SYMBL 

    insert_statement = "REPLACE INTO "+ stock_symbol +"_5min (t, v, c, h, l, o) VALUES (%s, %s, %s, %s, %s, %s)"
    mysql_connection.insert(insert_stmt=insert_statement, values=values)
    print("5min candle inserted")
        

if __name__=='__main__':
    # get_stock_news('AAPL')
    get_candle_5min('BINANCE:BTCUSDT')