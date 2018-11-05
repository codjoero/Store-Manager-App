from flask import Flask
from APIs.utilities import Utilities
from APIs.models.products import Product
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
        return 'Sale record created'

    @staticmethod
    def get_sale(table, column, value):
        """Method for retrieving a single product
        Returns a dictionary of the product that has been fetched.
        """
        sale = dbq.query_item(table, column, value)
        if sale == [] or sale is None:
            return False
        return sale

    @staticmethod
    def get_sale_products(item):
        cart = Sale.get_sale('sale_products', 'sale_id', item[0])#rows with sale_id
        for item in cart:


    @staticmethod
    def get_all_sales(sales, sale_products):
        """Method fetches all sales in the sales table
        Returns a list of all sales made.
        """
        sales_made = dbq.query_all_items(sales)
        # print (items)
        if sales == []:
            return False
        Sale.sales.clear()
        for item in sales_made:
            cart = Sale.get_sale_products(item)
            prod = Product.get_item('products', 'prod_id', cart[1])
            quantity = item[1] / prod[2]
            products = {
                'prod_id': prod[0],
                'prod_name': prod[1],
                'price': prod[2],
                'quantity': quantity
            }
            sale_dict = {
                'sale_id': item[0],
                'total_sale': item[1],
                'sold_by': item[2],
                'sale_date': item[3],
                'products': products, 
            }
            Sale.sales.append(sale_dict)
        return Sale.sales