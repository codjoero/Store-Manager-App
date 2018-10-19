
from flask import Flask, request, abort
from APIs.instance.util import Utilities

util = Utilities()

class Users:
    def __init__(self):
        self.users = []

    # products list enumaration
    def get_user_list(self, user_id):
        user = [user for user in self.users if user['user_id'] == user_id]
        if len(user) == 0:
            abort(404)
        return user

    def create_user(self):
        util.json_check('username')
        user = {
            "user_id": len(self.users) + 1,
            "name": request.json["name"],
            "username": request.json["username"],
            "password": request.json["password"],
            "grade": request.json["grade"]
        }
        self.users.append(user)
        return user

    def update_user(self, user_id):
        user = self.get_user_list(user_id)
        user[0]['name'] = request.json.get('name', user[0]['name'])
        user[0]['username'] = request.json.get('username', user[0]['username'])
        user[0]['password'] = request.json.get('passowrd', user[0]['password'])
        user[0]['grade'] = request.json.get('grade', user[0]['grade'])
        return user[0]

    def delete_user(self, user_id):
        user = self.get_user_list(user_id)
        self.users.remove(user[0])
        return True