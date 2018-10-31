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

    if not username or not user.valid_username():
        return jsonify({
            'message': 'Wrong username!'}), 400
    if not password or not user.valid_password():
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

# @app.route('/api/v1/users', methods=['POST'])
# def create_user():
#     return users.create_user()

# @app.route('/api/v1/users', methods=['GET'])
# def view_all_users():
#     return users.view_all_users()

# @app.route('/api/v1/users/<int:_id>', methods=['PUT'])
# def update_user(_id):
#     return users.update_user(_id)

# @app.route('/api/v1/users/<int:_id>', methods=['DELETE'])
# def delete_user(_id):
#     return users.delete_user(_id)