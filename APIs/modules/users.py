
from flask import Flask, request, abort
from APIs.instance.util import Utilities

util = Utilities()

class Users:
    def __init__(self):
        self.users = []


    def create_user(self):
        util.json_check('username')
        user = {
            "id": len(self.users) + 1,
            "name": request.json["name"],
            "username": request.json["username"],
            "password": request.json["password"],
            "grade": request.json["grade"]
        }
        self.users.append(user)
        return user

    def update_user(self, id):
        user = util.get_list_enum(self.users, id)
        return util.request_json_get(user)

    def delete_user(self, id):
        return util.general_delete(self.users, id)
