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
            print('Connected to {} successfully!'.format(self.db))
        except Exception as e:
            print(e)
            print('Successfully Failed to connect to database!')

if __name__ == '__main__':
    database_conn = DataBaseConnection()