from flask import Flask, request, jsonify, make_response
from APIs import app
from APIs.models.users import Users
from APIs.models.products import Products
from APIs.models.sales import Sales


users = Users()
products = Products()
sales = Sales()


"""Error Handlers 
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

@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'error': 'Server error'}), 500)


"""Root endpoint
"""
@app.route('/')
def welcome():
    return "Welcome!"


"""Users endpoints 
"""
@app.route('/storemanager/api/v1/users', methods=['POST'])
def create_user():
    return users.create_user()

@app.route('/storemanager/api/v1/users', methods=['GET'])
def view_all_users():
    return users.view_all_users()

@app.route('/storemanager/api/v1/users/<int:_id>', methods=['PUT'])
def update_user(_id):
    return users.update_user(_id)

@app.route('/storemanager/api/v1/users/<int:_id>', methods=['DELETE'])
def delete_user(_id):
    return users.delete_user(_id)



"""Products endpoints 
"""
@app.route('/storemanager/api/v1/products', methods=['POST'])
def create_product():
    return products.create_product()

@app.route('/storemanager/api/v1/products/<int:_id>', methods=['PUT'])
def update_product(_id):
    return products.update_product(_id)

@app.route('/storemanager/api/v1/products/<int:_id>', methods=['DELETE'])
def delete_product(_id):
    return products.delete_product(_id)

@app.route('/storemanager/api/v1/products/<int:_id>', methods=['GET'])
def view_a_product(_id):
    return products.view_a_product(_id)

@app.route('/storemanager/api/v1/products', methods=['GET'])
def view_all_product():
    return products.view_all_product()


 
"""Sales endpoints 
"""
@app.route('/storemanager/api/v1/sales', methods=['POST'])
def create_sale_order():
    return sales.create_sale_order()

@app.route('/storemanager/api/v1/sales/<int:_id>', methods=['GET'])
def get_sale_record(_id):
    return sales.get_sale_record(_id)

@app.route('/storemanager/api/v1/sales', methods=['GET'])
def get_all_sale_records():
    return sales.get_all_sale_records()