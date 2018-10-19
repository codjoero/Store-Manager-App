from flask import Flask, request, abort
import datetime
from APIs.instance.util import Utilities

util = Utilities()

class Products:
    def __init__(self):
        self.products = []

    # products list enumaration
    def get_prod_list(self, id):
        prod = [prod for prod in self.products if prod['prod_id'] == id]
        if len(prod) == 0:
            abort(404)
        return prod

    def create_product(self):
        util.json_check('prod_name')
        product = {
            "prod_id": len(self.products) + 1,
            "prod_name": request.json["prod_name"],
            "category": request.json["category"],
            "stock": request.json["stock"],
            "min_stock": request.json["min_stock"],
            "price": request.json["price"],
            "stock_date": datetime.date.today()
        }
        self.products.append(product)
        return product

    def update_product(self, prod_id):
        prod = self.get_prod_list(prod_id)
        if not request.json:
            abort(400)
        prod[0]['prod_name'] = request.json.get('prod_name', prod[0]['prod_name'])
        prod[0]['category'] = request.json.get('category', prod[0]['category'])
        prod[0]['stock'] = request.json.get('stock', prod[0]['stock'])
        prod[0]['min_stock'] = request.json.get('min_stock', prod[0]['min_stock'])
        prod[0]['price'] = request.json.get('price', prod[0]['price'])
        return prod[0]

    def delete_product(self, prod_id):
        prod = self.get_prod_list(prod_id)
        self.products.remove(prod[0])
        return True

    def view_a_product(self, id):
        return self.get_prod_list(id)

    def view_all_product(self):
        return self.products