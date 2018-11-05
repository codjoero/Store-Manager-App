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
        """Method for retrieving a single sale
        Returns a dictionary of the sale that has been fetched.
        """
        sale = dbq.query_item(table, column, value)
        if sale == [] or sale is None:
            return False
        cart = Sale.get_sale_products(sale)
        sale_dict = {
                'sale_id': sale[0],
                'total_sale': sale[1],
                'sold_by': sale[2],
                'sale_date': sale[3],
                'products': cart, 
            }
        return sale_dict

    @staticmethod
    def get_item(table, column, value):
        """Method for retrieving a single item
        Returns a dictionary of the item that has been fetched.
        """
        sale = dbq.query_item(table, column, value)
        if sale == [] or sale is None:
            return False
        return sale

    @staticmethod
    def get_sale_products(item):
        cart = Sale.get_item('sale_products', 'sale_id', item[0])#rows with sale_id
        print(cart)
        prod_sold = []
        prod = Product.get_item('products', 'prod_id', cart[1])
        quantity = item[1] / prod[4]
        product = {
            'prod_id': prod[0],
            'prod_name': prod[1],
            'price': prod[4],
            'quantity': quantity
        }
        prod_sold.append(product)
        return prod_sold

    @staticmethod
    def get_all_sales(sales):
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
            sale_dict = {
                'sale_id': item[0],
                'total_sale': item[1],
                'sold_by': item[2],
                'sale_date': item[3],
                'products': cart, 
            }
            Sale.sales.append(sale_dict)
        return Sale.sales