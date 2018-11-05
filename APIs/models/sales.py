from flask import Flask
from APIs.utilities import Utilities
from database.dbqueries import DbQueries
import datetime

dbq = DbQueries()
util = Utilities()
class Sale:
    """ Class handles sales
    """
    sales = []

    def __init__(self, prod_name, prod_id,quantity, total_sale,sold_by):
        self.prod_name = prod_name
        self.prod_id = prod_id
        self.quantity = quantity
        self.total_sale = total_sale
        self.sold_by = sold_by

    def add_sale(self):
        dbq.add_sale(self.total_sale, self.sold_by, self.prod_id)
        return 'created'