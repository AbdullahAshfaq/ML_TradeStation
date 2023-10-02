
# MySQL libraries
import mysql.connector



class MySQL_Class:
    def __init__(self, host, user, password, database) -> None:
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        # Used in functions
        self.mydb = None
        self.mycursor = None

    def connect(self):
        # MySQL Connection: Save data in mysql
        self.mydb = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.password,
        database=self.database
        )
        self.mycursor = self.mydb.cursor()

    def insert(self, insert_stmt, values):
        '''
        insert_stmt = "INSERT INTO BTCUSDT (uuid, ts, currentts, volume, price) VALUES (%s, %s,%s, %s,%s)"
        values = [("123", "123","123", "123","123"),("123", "123","123", "123","123")]
        '''
        self.connect()
        if type(values) is list:
            self.mycursor.executemany(insert_stmt, values)
        else:
            self.mycursor.execute(insert_stmt, values)
        self.mydb.commit()
        self.mydb.close() # Closing connection after every transaction

    def close_connection(self):
        self.mydb.close()

