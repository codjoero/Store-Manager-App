from flask import Flask, request, abort, jsonify
import datetime
from APIs.utilities import Utilities

util = Utilities()

class Products:
    """Class handles products views"""
    def __init__(self):
        self.products = []

    def create_product(self):
        util.json_check('prod_name')
        product = {
            "_id": len(self.products) + 1,
            "prod_name": request.json["prod_name"],
            "category": request.json["category"],
            "stock": request.json["stock"],
            "min_stock": request.json["min_stock"],
            "price": request.json["price"],
            "stock_date": datetime.date.today()
        }

        if ' ' in product['prod_name'] or not product['category'] or\
            not product['stock'] or not product['min_stock'] or\
            not product['price']:
            abort(400)
        
        if not isinstance(product['stock'], int) or\
            not isinstance(product['min_stock'], int) or\
            not isinstance(product['price'], int):
            return jsonify({'message': 'Numbers expected for units'}), 400

        self.products.append(product)
        return jsonify({'New product': product}), 201


    def update_product(self, _id):
        prod = util.get_list_enum(self.products, _id)
        if not request.json:
            abort(400)
        if 'prod_name' in request.json and type(request.json['prod_name']) != str:
            abort(400)
        if 'category' in request.json and type(request.json['category']) != str:
            abort(400)
        if 'stock' in request.json and type(request.json['stock']) is not int:
            abort(400)
        if 'min_stock' in request.json and type(request.json['min_stock']) is not int:
            abort(400)
        if 'price' in request.json and type(request.json['price']) is not int:
            abort(400)

        return jsonify({'Updated product': util.request_json_get(prod)}), 200


    def view_a_product(self, _id):
        return jsonify({'Product': util.get_list_enum(self.products, _id)}), 200

    def view_all_product(self):
        if len(self.products) == 0:
            return jsonify({'message': 'Inventory is empty!'}), 404
        return jsonify({'Products': self.products}), 200
        
    def delete_product(self, _id):
        return jsonify({'Product deleted': util.general_delete(self.products, _id)}), 200

    