from database.db import DataBaseConnection
import datetime
db = DataBaseConnection()
cursor = db.cursor
 
class DbQueries():

    def add_user(self, *args):
        """Method adds a new user to the database
        """
        name = args[0]
        username = args[1]
        password = args[2]
        role = args[3]

        add_user = """
        INSERT INTO users(name, username, password, role)
        VALUES ('{}', '{}', '{}', '{}');
        """.format(name, username, password, role)
        cursor.execute(add_user)

    def add_product(self, *args):
        """Method adds a new product to the database
        """
        prod_name = args[0]
        category = args[1]
        stock = args[2]
        price = args[3]
        added_by = args[4]

        add_product = """
        INSERT INTO products(prod_name, category, stock,\
                        price, added_by)\
        VALUES('{}', '{}', '{}', '{}', '{}');
        """.format(prod_name, category, stock, price, added_by)
        cursor.execute(add_product)

    def add_sale(self, *args):
        """Method adds a new sale to the database
        """
        prod_name = args[0]
        category = args[1]
        quantity = args[2]
        price = args[3]
        total_price = args[4]
        sold_by = args[5]

        add_sale = """
        INSERT INTO sales(prod_name, category, quantity, price,\
                        total_price, sold_by)\
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}');
        """.format(prod_name, category, quantity, price,\
                        total_price, sold_by)
        cursor.execute(add_sale)

    def query_item(self, *args):
        """Method to query items from tables, given a table name
        column and check value
        """
        table = args[0]
        column = args[1]
        value = args[2]
        query_item = """
        SELECT * FROM {} WHERE {} = '{}';
        """.format(table, column, value)
        cursor.execute(query_item)
        item = cursor.fetchone()
        return item


    def drop_table(self, table):
        """Method drops tables
        """
        drop_table = """
                    DROP TABLE {};
                    """.format(table)
        cursor.execute(drop_table)
