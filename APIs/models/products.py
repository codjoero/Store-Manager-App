from flask import Flask
from APIs.utilities import Utilities
from database.dbqueries import DbQueries
import datetime

dbq = DbQueries()
util = Utilities()

class Product:
    """Class handles product objects
    """
    products = []

    def __init__(self, prod_name, category, stock, price):
        self.prod_name = prod_name
        self.category = category
        self.stock = stock
        self.price = price

    def add_product(self):
        """Method adds product to the inventory
        """
        dbq.add_product(self.prod_name, self.category, self.stock, 
                        self.price)


    @staticmethod
    def get_item(table, column, value):
        """Method for retrieving a single product
        Returns a dictionary of the product that has been fetched.
        """
        product = dbq.query_item(table, column, value)
        if product == [] or product is None:
            return False
        if product[6] == True:
            return False
        return product

    @staticmethod
    def get_all_items(tb_of_items):
        """Method fetches all items in a table
        Returns a list of all items.
        """
        items = dbq.query_all_items(tb_of_items)
        if items == []:
            return False
        Product.products.clear()
        for item in items: 
            if item[6] == False:
                prod_dict = {
                    'prod_id': item[0],
                    'prod_name': item[1],
                    'category': item[2],
                    'stock': item[3],
                    'price': item[4],
                    'added_by': item[5],
                    'added_on': item[7]
                }
                Product.products.append(prod_dict)
        return Product.products
    
    def update_product(self, prod_id):
        """Method enables admin to update a product in Inventory.
        returns a dictionary of updated product.
        """
        prod = dbq.query_item('products', 'prod_id', prod_id)
        if prod is None:
            return False
        if prod[6] == True:
            return False
        dbq.update_columns(self.prod_name, self.category, self.stock, 
                        self.price, prod_id)
        product = dbq.query_item('products', 'prod_id', prod_id)
        return {
            'prod_id': product[0],
            'prod_name': product[1],
            'category': product[2],
            'stock': product[3],
            'price': product[4]
        }
        
    @classmethod
    def delete_product(self, prod_id):
        """Method enables admin to delete a product in Inventory,
        sets the delete_status to True.
        """
        dbq.update_a_col('delete_status', 'TRUE', prod_id)

