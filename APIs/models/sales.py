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

    def __init__(self, sale_prod_list, total_sale,sold_by):
        self.sale_prod_list = sale_prod_list
        self.total_sale = total_sale
        self.sold_by = sold_by

    def add_sale(self):
        sale_id = dbq.add_sale(self.total_sale, self.sold_by)
        for sale_prod in self.sale_prod_list:
            prod_id = sale_prod['prod_id']
            quantity = sale_prod['quantity']
            dbq.add_sale_products(sale_id, prod_id, quantity)
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
                'products': cart 
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
    def get_many(table, column, value):
        """Method for retrieving items
        Returns a list of the items that have been fetched.
        """
        sale = dbq.query_many(table, column, value)
        print(sale)
        if sale == [] or sale is None:
            return False
        return sale

    @staticmethod
    def get_sale_products(sale):
        prod_sold = []
        cart = Sale.get_many('sale_products', 'sale_id', sale[0]) #rows with sale_id
        for prod in cart:
            product = Product.get_item('products', 'prod_id', prod[1])
            # quantity = sale[1] / product[4]
            product = {
                'prod_id': product[0],
                'prod_name': product[1],
                'price': product[4],
                'quantity': prod[2]
            }
            prod_sold.append(product)
        return prod_sold

    @staticmethod
    def get_all_sales(sales):
        """Method fetches all sales in the sales table
        Returns a list of all sales made.
        """
        sales_made = dbq.query_all_items(sales)
        if sales_made == []:
            return False
        Sale.sales.clear()
        for sale in sales_made:
            cart = Sale.get_sale_products(sale)
            sale_dict = {
                'sale_id': sale[0],
                'total_sale': sale[1],
                'sold_by': sale[2],
                'sale_date': sale[3],
                'products': cart, 
            }
            Sale.sales.append(sale_dict)
        return Sale.sales