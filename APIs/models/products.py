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
        return product

    @staticmethod
    def get_all_items(tb_of_items):
        """Method fetches all items in the products table
        Returns a list of all products in Inventory.
        """
        items = dbq.query_all_items(tb_of_items)
        if items == []:
            return False
        else:
            Product.products.clear()
            for item in items:
                prod_dict = {
                    'prod_id': items[0],
                    'prod_name': items[1],
                    'category': items[2],
                    'stock': items[3],
                    'price': items[4],
                    'added_by': items[5],
                    'added_on': items[6]
                }
                Product.products.append(prod_dict)
        return Product.products
    