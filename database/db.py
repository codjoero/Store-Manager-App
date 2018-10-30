import psycopg2
import os

class DataBaseConnection:
    '''Class for database connection'''

    def __init__(self):
        try:
            if os.getenv('APP_SETTINGS') == 'testing' or 'development':
                self.db = 'test_db'
            else:
                self.db = 'deploy_db'
            self.conn = psycopg2.connect(dbname=self.db, user='codjoe',\
                    host='localhost', password='codjoe', port='5432')

            self.cursor = self.conn.cursor()
            self.conn.autocommit = True

            self.cursor.execute(
                """
                CREATE TABLE if not exists users (
                    _id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    time_stamp TIMESTAMPTZ DEFAULT NOW()
                )
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE if not exists products (
                    _id SERIAL PRIMARY KEY,
                    prod_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    stock INT NOT NULL,
                    min_stock INT NOT NULL,
                    price INT NOT NULL,
                    added_by TEXT NOT NULL,
                    time_stamp TIMESTAMPTZ DEFAULT NOW()
                )
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE if not exists sales (
                    _id SERIAL PRIMARY KEY,
                    prod_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    quantity INT NOT NULL,
                    price INT NOT NULL,
                    total_price INT NOT NULL,
                    sold_by TEXT NOT NULL,
                    sale_date TIMESTAMPTZ DEFAULT NOW()
                )
                """
            )
            print('Connected to {} successfully!'.format(self.db))

        except Exception as e:
            print(e)
            print('Successfully Failed to connect to database!')

    def drop_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS users CASCADE""")
        self.cursor.execute("""DROP TABLE IF EXISTS products CASCADE""")
        self.cursor.execute("""DROP TABLE IF EXISTS sales CASCADE""")

if __name__ == '__main__':
    database_conn = DataBaseConnection()