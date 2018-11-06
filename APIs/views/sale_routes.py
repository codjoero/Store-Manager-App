from flask import Flask, request, jsonify, make_response
from APIs import app
import datetime
import re
from APIs.views import user_routes, prod_routes, sale_routes
from APIs.models.users import User
from APIs.models.products import Product
from APIs.models.sales import Sale
from database.db import DataBaseConnection
from APIs.utilities import Utilities, SaleValidation
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)

db = DataBaseConnection()

@app.route('/api/v1/sales', methods=['POST'])
@jwt_required
def create_sale_order():
    """Method for sale attendant to add sales
    """
    auth_name = get_jwt_identity()
    auth_user = User.query_item('users', 'username', auth_name)
    if auth_user is False or auth_user[-2] != 'attendant':
        return jsonify({
            'message': 'Unauthorized Access!'
        }), 401
    try:
        products = request.json['products']
        # prod_name = request.json['prod_name']
        # quantity = request.json['quantity']
        # quantity = int(quantity)
    except KeyError:
        return jsonify({
            'Expected fields': {
                'prod_name': 'a string',
                'quantity': 'a number'
            }
        }), 400
    sale = SaleValidation(products)
    # sale = SaleValidation(prod_name, quantity)
    if not sale.valid_sale():
        return jsonify({
            'message': 'One of the fields is empty!'})
    if not sale.valid_types():
        return jsonify({
            'message': 'prod_name & quantity should be a character & number respectively!'})
    total_sale = 0
    prod_id_list = []
    for prod in products:
        product = Product.get_item('products', 'prod_name', prod['prod_name'])
        if not product:
            return jsonify({
                'message': 'This product is not in the Inventory!'}), 404
        elif product[3] <= 0:
            return jsonify({
                'message': '{} is out of stock!'.format(prod['prod_name'])
            }), 404
        elif product[3] < prod['quantity']:
                return jsonify({
                    'message': 'Only {} {} available right now!'.format(product[3], prod['prod_name'])
            }), 400
        prod_id = product[0]
        prod_id_list.append(prod_id)
        prod_sale = product[4] * prod['quantity']
        total_sale += prod_sale

    new_sale = Sale(prod_id_list, total_sale, auth_name)
    add_cart = new_sale.add_sale()
    return jsonify({
                'message': add_cart}), 200

@app.route('/api/v1/sales/<sale_id>', methods=['GET'])
@jwt_required
def get_sale_record(sale_id):
    """Method for admin / store attendant to view a specific sale.
    store attendant views sales made by only themselves
    returns a product that matches the given prod_id.
    """
    auth_name = get_jwt_identity()
    auth_user = User.query_item('users', 'username', auth_name)
    sale = Sale.get_sale('sales', 'sale_id', int(sale_id))
    try:
        if auth_user is False:
            return jsonify({
                'message': 'Unauthorized Access!'
            }), 401
        elif auth_user[-2] != 'admin' and auth_name != sale['sold_by']:
            return jsonify({
                'message': 'You have no access to this sale!'
            }), 401
    except TypeError:
        return jsonify({
            'message': 'This sale does not exist!'
        }), 400
    try:
        if not Sale.get_all_sales('sales'):
            return jsonify({
                'message': 'There are no sales yet!'
            }), 404
        sale = Sale.get_sale('sales', 'sale_id', int(sale_id))
        if not sale:
            return jsonify({
                'message': 'This sale does not exist!'
            }), 404
        return jsonify({
                'sale': sale}), 200
    except ValueError:
        return jsonify({
            'message': 'Try an interger for sale id'
        }), 400

@app.route('/api/v1/sales', methods=['GET'])
@jwt_required
def get_all_sale_records():
    """Method for admin to view all sale records.
    returns a list of all sales.
    """
    auth_name = get_jwt_identity()
    auth_user = User.query_item('users', 'username', auth_name)
    if auth_user is False or auth_user[-2] != 'admin':
        return jsonify({
            'message': 'Unauthorized Access!'
        }), 401
    sales = Sale.get_all_sales('sales')
    if not sales:
        return jsonify({
            'message': 'There are no sales yet!'
        }), 404
    return jsonify({
        'Sale Records': sales}), 200