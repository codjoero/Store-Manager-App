from flask import Flask, request, jsonify
from APIs import app
import datetime
from APIs.models.users import User
from database.db import DataBaseConnection
from APIs.utilities import Utilities, UserValidation
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt, get_jti)


@app.route('/api/v1/login', methods=['POST'])
def login():
    """Method for all users to log into the app
    Assigns a token if all checks out.
    """
    username = request.json['username']
    password = request.json['password']

    user = UserValidation('none', username, password)
    logged_user = User.query_item('users', 'username', username)
    if not user.valid_username():
        return jsonify({
            'message': 'Wrong username!'}), 400
    if not user.valid_password():
        return jsonify({
            'message': 'Wrong password!'}), 400
    elif not logged_user:
        return jsonify({
            'message': 'Wrong username!'}), 400
    elif not User.password_verification(username, password):
        return jsonify({
            'message': 'Wrong password!'}), 400
    token = create_access_token(
                identity=username, 
                expires_delta=datetime.timedelta(hours=1)
                )
    return jsonify({
            'token': token,
            'message': 'Login sucessful!',
            'user':dict(
                user_id=logged_user[0],
                name=logged_user[1],
                username=logged_user[2],
                role=logged_user[4],
                added_on=logged_user[5]
            )
            }), 200

@app.route('/api/v1/users', methods=['POST'])
@jwt_required
def create_user():
    """Method for admin to add store attendant account
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
        name = request.json['name']
        username = request.json['username']
        password = request.json['password']
        role = request.json['role']
    except KeyError:
        return jsonify({
            'message':'Please input all fields'
        }), 400

    user = UserValidation(name, username, password)

    if not name or not username or not password or not role:
        return jsonify({
            'message':'Please input all fields!'
        }), 400
    if 'admin' != role != 'attendant':
        return jsonify({
            'message':'role should either be admin or attendant'
        }), 400

    elif not user.valid_name():
        return jsonify({
            'message': 'Enter name in a correct string format, (john doe)!'
        }), 400
    elif not user.valid_username():
        return jsonify({
            'message': 'Enter username in a correct string format no spaces, (johndoe)!'
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

@app.route('/api/v1/logout', methods=['DELETE'])
@jwt_required
def logout():
    """Method for all users to logout of the app
    Token is blacklisted if still active.
    """
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        tk_jti = get_jti(auth_token)
        resp = User.logout(tk_jti)
        return resp
    else:
        return jsonify({
            'message': 'Unauthorized Access!'
        }), 401

# @app.route('/api/v1/users', methods=['GET'])
# def view_all_users():
#     return users.view_all_users()

# @app.route('/api/v1/users/<int:_id>', methods=['PUT'])
# def update_user(_id):
#     return users.update_user(_id)

# @app.route('/api/v1/users/<int:_id>', methods=['DELETE'])
# def delete_user(_id):
#     return users.delete_user(_id)