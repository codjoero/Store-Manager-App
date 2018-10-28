from flask import Flask, request, jsonify, make_response
from APIs import app
from APIs.models.products import Products

products = Products()


"""Products endpoints 
"""
@app.route('/api/v1/products', methods=['POST'])
def create_product():
    return products.create_product()

@app.route('/api/v1/products/<int:_id>', methods=['PUT'])
def update_product(_id):
    return products.update_product(_id)

@app.route('/api/v1/products/<int:_id>', methods=['DELETE'])
def delete_product(_id):
    return products.delete_product(_id)

@app.route('/api/v1/products/<int:_id>', methods=['GET'])
def view_a_product(_id):
    return products.view_a_product(_id)

@app.route('/api/v1/products', methods=['GET'])
def view_all_product():
    return products.view_all_product()