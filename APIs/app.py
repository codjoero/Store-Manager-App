
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
@app.route('/storemanager/api/v1/users', methods=['POST'])
def create_user():
    return jsonify({'New user': users.create_user()}), 201

@app.route('/storemanager/api/v1/users/<int:id>', methods=['PUT'])
def update_user(id):
    return jsonify({'Updated user': users.update_user(id)}), 200

@app.route('/storemanager/api/v1/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    return jsonify({'User Deleted': users.delete_user(id)}), 200

""" 
Products endpoints 
"""
@app.route('/storemanager/api/v1/products', methods=['POST'])
def create_product():
    return jsonify({'New product': products.create_product()}), 201

@app.route('/storemanager/api/v1/products/<int:id>', methods=['PUT'])
def update_product(id):
    return jsonify({'Updated product': products.update_product(id)}), 200

@app.route('/storemanager/api/v1/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    return jsonify({'Product Deleted': products.delete_product(id)}), 200

@app.route('/storemanager/api/v1/products/<int:id>', methods=['GET'])
def view_a_product(id):
    return jsonify({'Product': products.view_a_product(id)}), 200

@app.route('/storemanager/api/v1/products', methods=['GET'])
def view_all_product():
    return jsonify({'Products': products.view_all_product()}), 200

""" 
Sales endpoints 
"""
@app.route('/storemanager/api/v1/sales', methods=['POST'])
def create_sale_order():
    return jsonify({'New sale': sales.create_sale_order()}), 201

@app.route('/storemanager/api/v1/sales/<int:id>', methods=['GET'])
def get_sale_record(id):
    return jsonify({'New sale': sales.get_sale_record(id)}), 200

@app.route('/storemanager/api/v1/sales', methods=['GET'])
def get_all_sale_records():
    return jsonify({'Sale Record': sales.get_all_sale_records()}), 200

if __name__ == '__main__':
    app.run(debug=True)