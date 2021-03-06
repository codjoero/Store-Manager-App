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

        add_product = """
        INSERT INTO products(prod_name, category, stock, price)\
        VALUES('{}', '{}', '{}', '{}');
        """.format(prod_name, category, stock, price)
        cursor.execute(add_product)

    def add_sale(self, *args):
        """Method adds a new sale to the database
        """
        total_sale = args[0]
        sold_by = args[1]

        add_sale = """
        INSERT INTO sales(total_sale, sold_by)\
        VALUES ('{}', '{}')
        RETURNING sale_id;
        """.format(total_sale, sold_by)
        cursor.execute(add_sale)
        sale_id = cursor.fetchone()[0]
        return sale_id

    def add_sale_products(self, *args):
        """Method adds sale products to the database
        """
        sale_id = args[0]
        prod_id = args[1]
        quantity = args[2]

        add_sale_prod = """
        INSERT INTO sale_products(sale_id, prod_id, quantity)\
        VALUES ('{}', '{}', '{}')
        RETURNING sale_id;
        """.format(sale_id, prod_id, quantity)
        cursor.execute(add_sale_prod)

    def add_jti(self, jti):
        """Method adds a token jti to the database
        """
        add_jti = """
        INSERT INTO blacklisted_tokens(tk_jti)\
        VALUES ('{}');
        """.format(jti)
        cursor.execute(add_jti)

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

    def query_many(self, *args):
        """Method to query items with same sale_id from tables, 
        given a table name column and check value
        """
        table = args[0]
        column = args[1]
        value = args[2]
        query_item = """
        SELECT sale_id, prod_id, quantity FROM {} WHERE {} = '{}';
        """.format(table, column, value)
        cursor.execute(query_item)
        items = cursor.fetchall()
        return items

    def query_all_items(self, tb_of_items):
        """Method fetches all rows in a table
        """
        query_items = """
        SELECT * FROM {};
        """.format(tb_of_items)
        cursor.execute(query_items)
        items = cursor.fetchall()
        return items
    
    def update_columns(self, *args):
        """Method updates columns
        """
        prod_name = args[0]
        category = args[1]
        stock = args[2]
        price = args[3]
        prod_id = args[4]

        update_item = """
        UPDATE products SET prod_name='{}', category='{}', stock='{}', price ='{}'\
        WHERE prod_id='{}';
        """.format(prod_name, category, stock, price, prod_id)
        cursor.execute(update_item)

    def update_user(self, *args):
        """Method updates columns
        """
        name = args[0]
        username = args[1]
        password = args[2]
        role = args[3]
        user_id = args[4]

        update_user = """
        UPDATE users SET name='{}', username='{}', password='{}', role ='{}'\
        WHERE user_id='{}';
        """.format(name, username, password, role, user_id)
        cursor.execute(update_user)

    def update_a_col(self, *args):
        """Method updates a single column
        """
        col_name = args[0]
        col_value = args[1]
        prod_id = args[2]

        update_item = """
        UPDATE products SET {}='{}'\
        WHERE prod_id='{}';
        """.format(col_name, col_value, prod_id)
        cursor.execute(update_item)

    def delete_item(self, *args):
        table = args[0]
        column = args[1]
        value = args[2]
        delete_item = """
        DELETE FROM {} WHERE {} = '{}';
        """.format(table, column, value)
        cursor.execute(delete_item)

    def drop_table(self, table):
        """Method drops tables
        """
        drop_table = """
                    DROP TABLE {} CASCADE;
                    """.format(table)
        cursor.execute(drop_table)
