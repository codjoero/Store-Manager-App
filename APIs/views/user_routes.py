from flask import Flask, request, jsonify, make_response
from APIs import app
import datetime
from APIs.views import user_routes, prod_routes, sale_routes
from APIs.models.users import User
from database.db import DataBaseConnection
from APIs.utilities import Utilities, UserValidation
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)

db = DataBaseConnection()

@app.route('/api/v1/login', methods=['POST'])
def login():
    """Method for all users to log into the app
    Assigns a token if all checks out.
    """
    username = request.json['username']
    password = request.json['password']

    user = UserValidation('none', username, password)

    if not user.valid_username():
        return jsonify({
            'message': 'Wrong username!'}), 400
    if not user.valid_password():
        return jsonify({
            'message': 'Wrong password!'}), 400
    elif not User.query_item('users', 'username', username):
        return jsonify({
            'message': 'Wrong username!'}), 400
    elif not User.password_verification(username, password):
        return jsonify({
            'message': 'Wrong password!'}), 400
    token = create_access_token(identity=username)
    return jsonify({
            'token': token,
            'message': 'Login sucessful!'}), 200

@app.route('/api/v1/users', methods=['POST'])
@jwt_required
def create_user():
    """Method for admin to add store attendant account
    """
    auth_name = get_jwt_identity()
    auth_user = User.query_item('users', 'username', auth_name)
    if auth_user is False or auth_user[-2] != 'admin':
        return jsonify({
            'message': 'Unauthorized Access!'
        }), 401
    else:
        name = request.json['name']
        username = request.json['username']
        password = request.json['password']
        role = request.json['role']

        user = UserValidation(name, username, password)

        if not user.valid_name() or not user.valid_username():
            return jsonify({
                'message': 'Enter name / username in string format!'
            }), 400
        elif not user.valid_password():
            return jsonify({
                'message': 'Password should be longer than 6 characters, have atleast an uppercase and a lowercase!'
            }), 400
        elif User.query_item('users', 'name', name):
            return jsonify({
                'message': 'This name is already registered!'}), 400
        elif User.query_item('users', 'username', username):
            return jsonify({
                'message': 'This username is already taken!'}), 400

        user = User(name, username, password, role)
        hash_password = user.password_hash()
        user = User(name, username, hash_password, role)
        new_user = user.add_user()

        return jsonify({
            'message': '{} has been registered'.format(new_user)
        }), 201




# @app.route('/api/v1/users', methods=['GET'])
# def view_all_users():
#     return users.view_all_users()

# @app.route('/api/v1/users/<int:_id>', methods=['PUT'])
# def update_user(_id):
#     return users.update_user(_id)

# @app.route('/api/v1/users/<int:_id>', methods=['DELETE'])
# def delete_user(_id):
#     return users.delete_user(_id)