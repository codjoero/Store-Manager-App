from flask import Flask, request, jsonify, abort
import datetime
from APIs.utilities import Utilities

util = Utilities()

class Sales:
    """ Class handles sales views """
    def __init__(self):
        self.sales = []

    def create_sale_order(self):
        util.json_check('prod_name')
        sale = {
            "_id": len(self.sales) + 1,
            "prod_name": request.json["prod_name"],
            "category": request.json["category"],
            "quantity": request.json["quantity"],
            "price": request.json["price"],
            "sale_date": datetime.date.today()
        }

        if ' ' in sale['prod_name'] or not sale['category'] or\
            not sale['quantity'] or not sale['price']:
            abort(400)

        if not isinstance(sale['quantity'], int) or\
            not isinstance(sale['price'], int):
            return jsonify({'message': 'Numbers expected for units'}), 400

        self.sales.append(sale)
        return jsonify({'Sale Record': sale}), 201

    def get_sale_record(self, _id):
        return jsonify({'Sale record': util.get_list_enum(self.sales, _id)}), 200

    def get_all_sale_records(self):
        if len(self.sales) == 0:
            return jsonify({'message': 'No sale made yet!'}), 400
        return jsonify({'Sale records': self.sales}), 200