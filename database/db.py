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
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(500) NOT NULL,
                    role VARCHAR(255) NOT NULL,
                    added_on TIMESTAMPTZ DEFAULT NOW()
                )
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    prod_id SERIAL PRIMARY KEY,
                    prod_name VARCHAR(255) NOT NULL,
                    category VARCHAR(255) NOT NULL,
                    stock INT NOT NULL,
                    price INT NOT NULL,
                    added_by VARCHAR(25) DEFAULT 'admin',
                    delete_status BOOLEAN DEFAULT FALSE,
                    added_on TIMESTAMPTZ DEFAULT NOW()
                )
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sales (
                    sale_id SERIAL PRIMARY KEY,
                    total_sale INT NOT NULL,
                    sold_by VARCHAR(25) NOT NULL,
                    sale_date TIMESTAMPTZ DEFAULT NOW()
                )
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sale_products (
                    sale_id  INT NOT NULL,
                    FOREIGN KEY(sale_id) REFERENCES sales(sale_id),
                    prod_id  INT NOT NULL,
                    FOREIGN KEY(prod_id) REFERENCES products(prod_id),
                    added_on TIMESTAMPTZ DEFAULT NOW()
                )
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS blacklisted_tokens (
                    tk_id SERIAL PRIMARY KEY,
                    tk_jti VARCHAR(225) NOT NULL,
                    blacklisted_on TIMESTAMPTZ DEFAULT NOW()
                )
                """
            )

            print('Sucessfully connected to {}!'.format(self.db))

        except Exception as e:
            print(e)
            print('Miserably Failed to connect to database!')

if __name__ == '__main__':
    database_conn = DataBaseConnection()