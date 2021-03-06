from flask import Flask, request, jsonify, make_response, render_template
from APIs import app
import datetime
from APIs.views import user_routes, prod_routes, sale_routes
from APIs.models.users import User
from database.db import DataBaseConnection
from APIs.utilities import Utilities, UserValidation

db = DataBaseConnection()

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
@app.route('/', methods=['GET'])
def welcome():
    return render_template('index.html')

"""User account register
"""
@app.route('/api/v1/register', methods=['POST'])
def register():
    """Method for a user to add an account
    """
    name = request.json['name']
    username = request.json['username']
    password = request.json['password']
    role = request.json['role']

    user = User(name, username, password, role)
    valid_user = UserValidation(name, username, password)

    if not valid_user.valid_name() or not valid_user.valid_username():
        return jsonify({
            'message': 'Enter name / username in string format!'
        }), 400
    if not valid_user.valid_password():
        return jsonify({
            'message': 'Password should be longer than 6 characters, have atleast an uppercase and a lowercase!'
        }), 400
      
    user = User(name, username, password, role)
    hash_password = user.password_hash()
    user = User(name, username, hash_password, role)
    new_user = user.add_user()

    if not new_user:
        return jsonify({
            'message': f'{username} is already registered!'
        }), 400
    return jsonify({
        'message': f'{new_user} has been registered'
    }), 201
