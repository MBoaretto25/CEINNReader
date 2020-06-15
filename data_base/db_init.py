import sqlite3
from sqlite3 import Error

import pandas


class TempDataBase:

    def __init__(self, db_local=None):
        self._db_local = db_local

        self._conn = None
        self._table_name = "transactions"

        self._create_connection()
        self._create_table()

    def _create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            if self._db_local:
                db_local = self._db_local
                conn = sqlite3.connect(db_local)
            else:
                conn = sqlite3.connect(':memory:')
        except Error as e:
            print(e)

        self._conn = conn

    def _create_table(self):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self._conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS {} (
                        date text, 
                        cv text, 
                        symbol text, 
                        quantity int, 
                        price real, 
                        total_price real
                        )'''.format(self._table_name))

        except Error as e:
            print(e)

    def insert_value(self, value):
        transactions = []

        if type(value) == pandas.core.frame.DataFrame:
            for idx, rows in value.iterrows():
                transactions.append([
                    rows[0].strip(),
                    rows[1].strip(),
                    rows[2].strip(),
                    rows[3], rows[4], rows[5]
                ])

        if type(value) == pandas.core.frame.Series:
            transactions.append([
                value[0].strip(),
                value[1].strip(),
                value[2].strip(),
                value[3], value[4], value[5]
            ])

        try:
            c = self._conn.cursor()
            c.executemany('INSERT INTO {} VALUES (?,?,?,?,?,?)'.format(self._table_name),
                          transactions)
        except Error as e:
            print(e)

    def show_table(self):
        c = self._conn
        for row in c.execute('SELECT * FROM {} ORDER BY date'.format(self._table_name)):
            print(row)

    def create_querry(self, querry):
        try:
            c = self._conn.cursor()
            querry = c.execute(querry)
            return querry
        except Error as e:
            print("Querrying Erros : {}".format(e))

    def close_table(self):
        self._conn.close()
