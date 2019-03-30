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
                expires_delta=datetime.timedelta(days=60)
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
    added_user = User.query_item('users', 'username', username)

    return jsonify({
        'message': '{} has been registered'.format(new_user),
        'user':dict(
                user_id=added_user[0],
                name=added_user[1],
                username=added_user[2],
                role=added_user[4],
                added_on=added_user[5]
            )
    }), 201

@app.route('/api/v1/users', methods=['GET'])
@jwt_required
def view_all_users():
    """Method for admin to view all user accounts.
    returns a list of creaetd user accounts.
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
    users = User.get_all_users('users')
    return jsonify({
        'users': users}), 200

@app.route('/api/v1/users/<user_id>', methods=['PUT'])
@jwt_required
def edit_user(user_id):
    """Method for admin to modify the details of a user.
    returns dictionary of updated user.
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
    try:
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
    
        user = User(name, username, password, role)
        hash_password = user.password_hash()
        user = User(name, username, hash_password, role)
        updated_user = user.update_user(int(user_id))
        if not updated_user:
            return jsonify({
                'message': "This user doesn't exist!"}), 400
        return jsonify({
            'message': 'user updated!',
            'User': updated_user
            }), 200
    except ValueError:
        return jsonify({
            'message': 'User_id should be numbers!'
        }), 400

@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
@jwt_required
def delete_user(user_id):
    """Method for admin to delete a user.
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
        user_id = int(user_id)
        users = User.get_all_users('users')
        if not users:
            return jsonify({
                'message': 'There are no store attendants added!'}), 404
        elif not User.query_item('users', 'user_id', user_id):
            return jsonify({
                'message': 'This attendant does not exist!'}), 404
        User.delete_user(user_id)
        return jsonify({
            'message': 'User deleted!'
        }), 200
    except ValueError:
        return jsonify({
            'message': 'The user id should be a number!'}), 400

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