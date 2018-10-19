from flask import Flask, request, abort
import datetime
from APIs.instance.util import Utilities

util = Utilities()

class Sales:
    def __init__(self):
        self.sales = []
        

    def create_sale_order(self):
        util.json_check('prod_name')
        sale = {
            "id": len(self.sales) + 1,
            "prod_name": request.json["prod_name"],
            "category": request.json["category"],
            "price": request.json["price"],
            "sale_date": datetime.date.today()
        }
        self.sales.append(sale)
        return sale

    def get_sale_record(self, id):
        return util.get_list_enum(self.sales, id)

    def get_all_sale_records(self):
        return self.sales