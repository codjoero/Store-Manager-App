
from flask import Flask, request, jsonify, abort, make_response
import json
from APIs.modules.users import Users
from APIs.modules.products import Products
from APIs.modules.sales import Sales


users = Users()
products = Products()
sales = Sales()

app = Flask(__name__)

app.secret = 'andela'
""" 
Error Handlers 
"""
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized'}), 401)


""" 
Users endpoints 
"""

@app.route('/')
def welcome():
    return "Welcome!"

@app.route('/storemanager/api/v1/users', methods=['POST'])
def create_user():
    return users.create_user()

@app.route('/storemanager/api/v1/users/<int:id>', methods=['PUT'])
def update_user(id):
    return users.update_user(id)

@app.route('/storemanager/api/v1/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    return users.delete_user(id)


""" 
Products endpoints 
"""
@app.route('/storemanager/api/v1/products', methods=['POST'])
def create_product():
    return products.create_product()

@app.route('/storemanager/api/v1/products/<int:id>', methods=['PUT'])
def update_product(id):
    return products.update_product(id)

@app.route('/storemanager/api/v1/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    return products.delete_product(id)

@app.route('/storemanager/api/v1/products/<int:id>', methods=['GET'])
def view_a_product(id):
    return products.view_a_product(id)

@app.route('/storemanager/api/v1/products', methods=['GET'])
def view_all_product():
    return products.view_all_product()


""" 
Sales endpoints 
"""
@app.route('/storemanager/api/v1/sales', methods=['POST'])
def create_sale_order():
    return sales.create_sale_order()

@app.route('/storemanager/api/v1/sales/<int:id>', methods=['GET'])
def get_sale_record(id):
    return sales.get_sale_record(id)

@app.route('/storemanager/api/v1/sales', methods=['GET'])
def get_all_sale_records():
    return sales.get_all_sale_records()


if __name__ == '__main__':
    app.run(debug=True)