from flask import Flask, request, jsonify
import datetime
from APIs.instance.util import Utilities

util = Utilities()

class Sales:
    def __init__(self):
        self.sales = []

    def create_sale_order(self):
        util.json_check('prod_name')
        sale = {
            "_id": len(self.sales) + 1,
            "prod_name": request.json["prod_name"],
            "category": request.json["category"],
            "price": request.json["price"],
            "sale_date": datetime.date.today()
        }
        self.sales.append(sale)
        return jsonify({'Sale Record': sale}), 201

    def get_sale_record(self, _id):
        return jsonify({'Sale record': util.get_list_enum(self.sales, _id)}), 200

    def get_all_sale_records(self):
        return jsonify({'Sale records': self.sales}), 200