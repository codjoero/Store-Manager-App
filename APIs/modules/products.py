from flask import Flask, request, abort
import datetime
from APIs.instance.util import Utilities

util = Utilities()

class Products:
    def __init__(self):
        self.products = []

    # # products list enumaration
    # def get_prod_list(self, id):
    #     prod = [prod for prod in self.products if prod['prod_id'] == id]
    #     if len(prod) == 0:
    #         abort(404)
    #     return prod

    def create_product(self):
        util.json_check('prod_name')
        product = {
            "id": len(self.products) + 1,
            "prod_name": request.json["prod_name"],
            "category": request.json["category"],
            "stock": request.json["stock"],
            "min_stock": request.json["min_stock"],
            "price": request.json["price"],
            "stock_date": datetime.date.today()
        }
        self.products.append(product)
        return product

    def update_product(self, id):
        prod = util.get_list_enum(self.products, id)
        if not request.json:
            abort(400)
        return util.request_json_get(prod)

    def delete_product(self, id):
        prod = util.get_list_enum(self.products, id)
        self.products.remove(prod[0])
        return True

    def view_a_product(self, id):
        return util.get_list_enum(self.products, id)

    def view_all_product(self):
        return self.products