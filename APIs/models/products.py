from flask import Flask
from APIs.utilities import Utilities
from database.dbqueries import DbQueries
import datetime

dbq = DbQueries()
util = Utilities()

class Product:
    """Class handles product objects
    """
    def __init__(self, prod_name, category, stock, price, added_by):
        self.prod_name = prod_name
        self.category = category
        self.stock = stock
        self.price = price
        self.added_by = added_by

    def add_product(self):
        """Method adds product to the inventory
        """
        dbq.add_product(self.prod_name, self.category, self.stock, 
                        self.price, self.added_by)
    