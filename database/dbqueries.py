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
        INSERT INTO users(name, username, password, admin)
        VALUES ('{}', '{}', '{}', '{}');
        """.format(name, username, password, role)
        cursor.execute(add_user)

    def add_product(self, *args):
        """Method adds a new product to the database
        """
        prod_name = args[0]
        category = args[1]
        stock = args[2]
        min_stock = args[3]
        price = args[4]
        added_by = args[5]

        add_product = """
        INSERT INTO products(prod_name, category, stock,\
                        min_stock, price)\
        VALUES('{}', '{}', '{}', '{}', '{}', '{}');
        """.format(prod_name, category, stock, min_stock,\
                    price, added_by)
        cursor.execute(add_product)

    def add_sale(self, *args):
        """Method adds a new sale to the database
        """
        prod_name = args[0]
        category = args[1]
        quantity = args[2]
        price = args[3]
        total_price = args[4]
        sold_by = args[4]

        add_sale = """
        INSERT INTO sales(prod_name, category, quantity, price,\
                        total_price, sold_by)\
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}');
        """.format(prod_name, category, quantity, price,\
                        total_price, sold_by)
        cursor.execute(add_sale)

    def drop_table(self, table):
        """Method drops tables
        """
        drop_table = """
                    DROP TABLE {};
                    """.format(table)
        cursor.execute(drop_table)
