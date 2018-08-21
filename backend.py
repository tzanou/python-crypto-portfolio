import sqlite3


class Database:

    def __init__(self,db):
        self.conn=sqlite3.connect(db)
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS investments (id INTEGER PRIMARY KEY, name TEXT,symbol TEXT,"
                         " amount REAL,price_bought REAL ,currency TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS coin_names (id INTEGER PRIMARY KEY, name TEXT,symbol TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS coins (id INTEGER PRIMARY KEY, name TEXT,symbol TEXT,"
                         " price REAL ,day_volume REAL,market_cap REAL,"
                         "available_supply REAL,open REAL,high REAL,"
                         "low REAL,currency TEXT,last_updated TEXT)")
        self.conn.commit()

    def insert_investment(self,name,symbol,amount,price_bought,currency):
        self.cur.execute("INSERT OR IGNORE INTO investments VALUES(null,?,?,?,?,?)",(name,symbol,amount,price_bought,currency))
        self.conn.commit()

    def insert_coin_name(self, name, symbol):
        self.cur.execute("INSERT OR IGNORE INTO coin_names VALUES(null,?,?)", (name, symbol))
        self.conn.commit()

    def get_number_of_coins(self):
        self.cur.execute("SELECT count(*) FROM coin_names ")
        rows = self.cur.fetchone()
        self.conn.commit()
        return rows[0]

    def insert_investment(self,investment):
        symbol=self.get_coin_symbol(investment.name.upper())
        self.cur.execute("INSERT OR IGNORE INTO investments VALUES(null,?,?,?,?,?)",(investment.name,symbol,investment.amount,investment.price_bought,investment.currency))
        self.conn.commit()

    def update_investment(self, investment,amount,price):
        self.cur.execute("UPDATE investments SET amount=?, price_bought=? WHERE id=?",(amount,price,investment[0]))
        self.conn.commit()

    def delete_investment(self, id):
        self.cur.execute("DELETE  FROM investments WHERE id=?",(id,))
        self.conn.commit()

    def insert_coin(self,name,symbol,price,day_volume,market_cap,available_supply,open,high,low,currency,last_updated):
        self.cur.execute("INSERT OR REPLACE INTO coins VALUES(null,?,?,?,?,?,?,?,?,?,?,?)",(name,symbol,price,day_volume,market_cap,available_supply,open,high,low,currency,last_updated))
        self.cur.execute("UPDATE coins SET price=?,day_volume=?,market_cap=?,available_supply=?,open=?,high=?,low=?,currency=? , last_updated=? where symbol=?",(price,day_volume,market_cap,available_supply,open,high,low,currency,last_updated,symbol))

        self.conn.commit()

    def get_coin_names(self):
        self.cur.execute("SELECT name FROM coins ")
        rows = self.cur.fetchall()
        self.conn.commit()

        to_return =[]
        for object in rows:
            to_return.append(object[0].lower())

        return to_return

    def get_coin_symbols(self):
        self.cur.execute("SELECT symbol FROM coin_names ")
        rows = self.cur.fetchall()
        self.conn.commit()

        to_return = []
        for object in rows:
            to_return.append(object[0])

        return to_return

    def get_investments_symbols(self):
        self.cur.execute("SELECT DISTINCT symbol FROM investments ")
        rows = self.cur.fetchall()
        self.conn.commit()

        to_return = []
        for object in rows:
            to_return.append(object[0])

        return to_return

    def get_investments_currencies(self):
        self.cur.execute("SELECT DISTINCT currency FROM investments ")
        rows = self.cur.fetchall()
        self.conn.commit()

        to_return = []
        for object in rows:
            to_return.append(object[0])

        return to_return

    def get_coin_value(self,symbol):
        print("getting value of "+ symbol)
        self.cur.execute("SELECT price FROM coins WHERE symbol like ? ", (symbol,))
        rows = self.cur.fetchone()
        self.conn.commit()
        return rows[0]

    def get_coin_value_from_symbol(self,symbol):
        self.cur.execute("SELECT price_usd FROM coins WHERE name like ? ", (symbol,))
        rows = self.cur.fetchone()
        self.conn.commit()
        return rows[0]

    def get_investments(self):
        self.cur.execute("SELECT * FROM investments ")
        rows = self.cur.fetchall()
        self.conn.commit()
        print (rows)
        return rows

    def get_number_of_investments(self):
        self.cur.execute("SELECT count(*) FROM investments ")
        rows = self.cur.fetchone()
        self.conn.commit()
        return rows[0]

    def get_coin_symbol(self,name):
        self.cur.execute("SELECT symbol FROM coin_names WHERE name like ? ",(name,))
        rows = self.cur.fetchone()

        self.conn.commit()
        print (rows)
        return rows[0]

    def get_coin_name(self,symbol):
        self.cur.execute("SELECT name FROM coin_names WHERE symbol like ? ",(symbol,))
        rows = self.cur.fetchone()
        self.conn.commit()
        return rows[0]

    def __del__(self):
        self.conn.close()
