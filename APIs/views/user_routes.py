from flask import Flask, request, jsonify, make_response
from APIs import app
import APIs.views
from APIs.models.users import Users

users = Users()


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
