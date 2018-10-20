from flask import Flask, request, abort, jsonify
import datetime
from APIs.instance.util import Utilities

util = Utilities()

class Products:
    def __init__(self):
        self.products = []

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
        return jsonify({'New product': product}), 201

    def update_product(self, id):
        prod = util.get_list_enum(self.products, id)
        if not request.json:
            abort(400)
        return jsonify({'Updated product': util.request_json_get(prod)}), 200

    def delete_product(self, id):
        return jsonify({'Product deleted': util.general_delete(self.products, id)}), 200

    def view_a_product(self, id):
        return jsonify({'Product': util.get_list_enum(self.products, id)}), 200

    def view_all_product(self):
        return jsonify({'Products': self.products}), 200