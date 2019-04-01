from flask import Flask, request, jsonify, make_response
from APIs import app
import datetime
import re
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
    if not User.valid_token(request.headers):
        return jsonify({
            'message': 'Invalid Authentication, Please Login!'
        }), 401
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
                'category': 'a string',
                'stock': 'a number',
                'price': 'a number'
            }
        }), 400

    prod = ProductValidation(prod_name, category, stock, price)
    if not prod_name or not category or not stock or not price:
        return jsonify({
            'message': 'Please enter all fields!'}), 400
    invalid_name = re.search(r"[0-9]", prod_name)
    invalid_category = re.search(r"[0-9]", category)
    if invalid_name or invalid_category:
        return jsonify({
            'message': 'Please enter strings in name and category!'}), 400
    if not prod.valid_product or not prod.valid_prod_fields:
        return jsonify({
            'message': 'Some fields are wrong or missing!'}), 400
    elif not isinstance(prod_name, str) or not isinstance(category, str):
        return jsonify({
            'message': 'prod_name and category must be characters!'}), 400
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
def view_a_product(prod_id):
    """Method for admin / store attendant to view a specific product.
    returns a product that matches the given prod_id.
    """
    try:
        if not Product.get_all_items('products'):
            return jsonify({
                'message': 'There are no products yet!'
            }), 204
        
        product = Product.get_item('products', 'prod_id', int(prod_id))
        if not product:
            return jsonify({
                'message': 'This product does not exist!'
            }), 204
        return jsonify({
            'product': {
                        'prod_id': product[0],
                        'prod_name': product[1],
                        'category': product[2],
                        'stock': product[3],
                        'price': product[4],
                        'added_by': product[5],
                        'added_on': product[7]
                    }
            }), 200
    except ValueError:
        return jsonify({
            'message': 'Try an interger for product id'
        }), 400

@app.route('/api/v1/products', methods=['GET'])
def view_all_product():
    """Method for admin / store attendant to view all products.
    returns a list products in the Inventory.
    """
    product = Product.get_all_items('products')
    if not product:
        return jsonify({
            'message': 'There are no products yet!'
        }), 204
    return jsonify({
        'products': product}), 200


@app.route('/api/v1/products/<int:prod_id>', methods=['PUT'])
@jwt_required
def update_product(prod_id):
    """Method for admin to modify the details of a product.
    returns dictionary of updated product.
    """
    if not User.valid_token(request.headers):
        return jsonify({
            'message': 'Invalid Authentication, Please Login!'
        }), 401
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
    except Exception:
        return jsonify({
            'Expected fields': {
                'prod_name': 'a string',
                'category': 'a string',
                'stock': 'a number',
                'price': 'a number'
            }
        }), 400
    try:
        prod = ProductValidation(prod_name, category, stock, price)
        if not prod.valid_product or not prod.valid_prod_fields:
            return jsonify({
            'message': 'Some fields are wrong or missing!'}), 400
        if not prod_name or not category:
            return jsonify({
            'message': 'prod_name and category cannot be empty!'}), 400
        elif not isinstance(prod_name, str) or not isinstance(category, str):
            return jsonify({
            'message': 'prod_name and category should be characters!'}), 400
        elif not isinstance(stock, int) or not isinstance(price, int):
            return jsonify({
            'message': 'The Stock and Price must be numbers!'}), 400
        

        product = Product(prod_name, category, stock, price)
        prod = product.update_product(prod_id)
        if not prod:
            return jsonify({
                'message': "This product doesn't exists in the Inventory!"}), 204
        return jsonify({
            'message': 'product updated!',
            'Product': prod
            }), 200
    except ValueError:
        return jsonify({
            'message': 'Prod_id, stock and price should be numbers!'
        }), 400

@app.route('/api/v1/products/<prod_id>', methods=['DELETE'])
@jwt_required
def delete_product(prod_id):
    """Method for admin to delete a product.
    returns message of successful deletion.
    """
    if not User.valid_token(request.headers):
        return jsonify({
            'message': 'Invalid Authentication, Please Login!'
        }), 401
    auth_name = get_jwt_identity()
    auth_user = User.query_item('users', 'username', auth_name)
    if auth_user is False or auth_user[-2] != 'admin':
        return jsonify({
            'message': 'Unauthorized Access!'
        }), 401

    try:
        prod_id = int(prod_id)
        product = Product.get_all_items('products')
        if not product:
            return jsonify({
                'message': 'There are no products in Inventory!'}), 204
        elif not Product.get_item('products', 'prod_id', prod_id):
            return jsonify({
                'message': 'This product does not exist in Inventory!'}), 204
        Product.delete_product(prod_id)
        return jsonify({
            'message': 'Product deleted!'
        }), 200
    except ValueError:
        return jsonify({
            'message': 'The product id should be a number!'}), 400