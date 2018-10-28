
from flask import Flask, request, jsonify, abort
from APIs.utilities import Utilities

util = Utilities()

class Users:
    """ Class handles users views """
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

        if util.duplicate_item(self.users, user, "username"):
            return jsonify({"message":"user already exists!"}), 400

        if not user['name'] or not user['username'] or\
            not user['password'] or not user['grade']:
            abort(400)
        
        if not isinstance(user['grade'], str):
            return jsonify({
                'message': 'Grade should be a string'
                }), 400

        self.users.append(user)
        return jsonify({'New Attendant': user}), 201

    def update_user(self, _id):
        user = util.get_list_enum(self.users, _id)
        if not request.json:
            abort(400)
        if 'name' in request.json and type(request.json['name']) != str:
            abort(400)
        if 'grade' in request.json and type(request.json['grade']) != str:
            abort(400)
        return jsonify({'Attendant updated': util.request_json_get(user)}), 200

    def view_all_users(self):
        if len(self.users) == 0:
            return jsonify({'message': 'No attendants added!'}), 400
        return jsonify({'Store Attendants': self.users}), 200

    def delete_user(self, _id):
        return jsonify({'Attendant Deleted': util.general_delete(self.users, _id)}), 200
