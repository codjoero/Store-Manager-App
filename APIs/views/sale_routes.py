from flask import Flask, request, jsonify, make_response
from APIs import app
from APIs.models.sales import Sales

sales = Sales()


"""Sales endpoints 
"""
@app.route('/api/v1/sales', methods=['POST'])
def create_sale_order():
    return sales.create_sale_order()

@app.route('/api/v1/sales/<int:_id>', methods=['GET'])
def get_sale_record(_id):
    return sales.get_sale_record(_id)

@app.route('/api/v1/sales', methods=['GET'])
def get_all_sale_records():
    return sales.get_all_sale_records()