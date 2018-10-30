from flask import Flask, request, jsonify, make_response
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
@app.route('/')
def welcome():
    return "Welcome!"

"""Admin account register
"""
@app.route('/api/v1/register', methods=['POST'])
def register():
    """Method for admin to add an Admin account
    """
    name = request.json['name']
    username = request.json['username']
    password = request.json['password']
    time_stamp = datetime.datetime.now()
    admin = True

    user = UserValidation(name, username, password)

    if not user.valid_name() or user.valid_username():
        return jsonify({
            'message': 'Enter name / username in string format!'
        }), 400
    elif not user.valid_password():
        return jsonify({
            'message': 'Password should be longer than 6 characters,\
            have atleast an uppercase and a lowercase!'
        }), 400
    # elif user.duplicate():
    #     pass

    user = User(name, username, password, time_stamp, admin)
    hash_password = user.password_hash()
    user = User(name, username, hash_password, time_stamp, admin)
    new_user = user.add_user()

    return jsonify({
        'message': '{} has been registered'.format(new_user)
    }), 201
