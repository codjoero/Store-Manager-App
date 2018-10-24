
from flask import Flask, request, jsonify
from APIs.instance.util import Utilities

util = Utilities()

class Users:
    def __init__(self):
        self.users = []


    def create_user(self):
        util.json_check('username')
        user = {
            "_id": len(self.users) + 1,
            "name": request.json["name"],
            "username": request.json["username"],
            "password": request.json["password"],
            "grade": request.json["grade"]
        }
        self.users.append(user)
        return jsonify({'New user': user}), 201

    def update_user(self, _id):
        user = util.get_list_enum(self.users, _id)
        return jsonify({'New user': util.request_json_get(user)}), 200

    def delete_user(self, _id):
        return jsonify({'User Deleted': util.general_delete(self.users, _id)}), 200
