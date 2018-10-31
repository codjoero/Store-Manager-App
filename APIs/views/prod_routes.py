from flask import Flask, request, jsonify, make_response
from APIs import app
import datetime
from APIs.views import user_routes, prod_routes, sale_routes
from APIs.models.users import User
from APIs.models.products import Product
from database.db import DataBaseConnection
from APIs.utilities import Utilities, UserValidation, ProductValidation
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)

db = DataBaseConnection()

@app.route('/api/v1/products', methods=['POST'])
@jwt_required
def create_product():
    """Method for admin to add product to inventory
    """
    auth_name = get_jwt_identity()
    auth_user = User.query_item('users', 'username', auth_name)
    if auth_user is False or auth_user[-2] != 'admin':
        return jsonify({
            'message': 'Unauthorized Access!'
        }), 401
    else:
        prod_name = request.json['prod_name']
        category = request.json['category']
        stock = request.json['stock']
        price = request.json['price']
        added_by = request.json['added_by']

        prod = ProductValidation(prod_name, category, stock,\
                    price, added_by)
        if not prod.valid_product:
            return jsonify({
                'message': 'Some fields are wrong or missing!'}), 400
        elif not isinstance(prod_name, str) or not isinstance(category, str)\
                            or not isinstance(added_by, str):
            return jsonify({
                'message': '[prod_name, category, added_by] should be characters!'}), 400
        elif not isinstance(stock, int) or not isinstance(price, int):
            return jsonify({
                'message': 'The Stock and Price must be numbers!'}), 400

        product = Product(prod_name, category, stock, price, added_by)
        if User.query_item('products', 'prod_name', prod_name):
            return jsonify({
                'message': 'This product exists in the Inventory!'
            })
        else:
            product.add_product()
            return jsonify({
            'message': 'Product successfully added to Inventory!'}), 201





# @app.route('/api/v1/products/<int:_id>', methods=['PUT'])
# def update_product(_id):
#     return products.update_product(_id)

# @app.route('/api/v1/products/<int:_id>', methods=['DELETE'])
# def delete_product(_id):
#     return products.delete_product(_id)

# @app.route('/api/v1/products/<int:_id>', methods=['GET'])
# def view_a_product(_id):
#     return products.view_a_product(_id)

# @app.route('/api/v1/products', methods=['GET'])
# def view_all_product():
#     return products.view_all_product()