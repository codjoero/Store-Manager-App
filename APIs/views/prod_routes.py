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
    try:
        prod_name = request.json['prod_name']
        category = request.json['category']
        stock = request.json['stock']
        price = request.json['price']
    except KeyError:
        return jsonify({
            'Expected fields': {
                'prod_name': 'a string',
                'category': 'characters',
                'stock': 'a string',
                'price': 'a string'
            }
        }), 400

    prod = ProductValidation(prod_name, category, stock, price)
    if not prod.valid_product:
        return jsonify({
            'message': 'Some fields are wrong or missing!'}), 400
    elif not isinstance(prod_name, str) or not isinstance(category, str):
        return jsonify({
            'message': '[prod_name, category, addesd_by] should be characters!'}), 400
    elif not isinstance(stock, int) or not isinstance(price, int):
        return jsonify({
            'message': 'The Stock and Price must be numbers!'}), 400

    product = Product(prod_name, category, stock, price)
    if User.query_item('products', 'prod_name', prod_name):
        return jsonify({
            'message': 'This product exists in the Inventory!'
        }), 400
    else:
        product.add_product()
        return jsonify({
        'message': 'Product successfully added to Inventory!'}), 201


@app.route('/api/v1/products/<prod_id>', methods=['GET'])
@jwt_required
def view_a_product(prod_id):
    """Method for admin / store attendant to view a specific product.
    returns a product that matches the given prod_id.
    """
    auth_name = get_jwt_identity()
    auth_user = User.query_item('users', 'username', auth_name)
    if auth_user is False:
        return jsonify({
            'message': 'Unauthorized Access!'
        }), 401
    try:
        if not Product.get_all_items('products'):
            return jsonify({
                'message': 'There are no products yet!'
            }), 404
        
        product = Product.get_item('products', 'prod_id', int(prod_id))
        if not product:
            return jsonify({
                'message': 'This product does not exist!'
            }), 404
        return jsonify({
            'product': {
                        'prod_id': product[0],
                        'prod_name': product[1],
                        'category': product[2],
                        'stock': product[3],
                        'price': product[4],
                        'added_by': product[5],
                        'added_on': product[6]
                    }
            }), 200
    except ValueError:
        return jsonify({
            'message': 'Try an interger for product id'
            }), 400

@app.route('/api/v1/products', methods=['GET'])
@jwt_required
def view_all_product():
    """Method for admin / store attendant to view all products.
    returns a list products in the Inventory.
    """
    auth_name = get_jwt_identity()
    auth_user = User.query_item('users', 'username', auth_name)
    if auth_user is False:
        return jsonify({
            'message': 'Unauthorized Access!'
        }), 401

    product = Product.get_all_items('products')
    if not product:
        return jsonify({
            'message': 'There are no products yet!'
        }), 404
    return jsonify({
        'products': product}), 200


# @app.route('/api/v1/products/<int:_id>', methods=['PUT'])
# def update_product(_id):
#     return products.update_product(_id)

# @app.route('/api/v1/products/<int:_id>', methods=['DELETE'])
# def delete_product(_id):
#     return products.delete_product(_id)
