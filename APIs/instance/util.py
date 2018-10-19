
from flask import Flask, request, jsonify, abort, make_response
import json


class Utilities():

    # Json input check for all methods
    def json_check(self, item):
        if not request.json or not item in request.json:
            abort(400)

    # List enumeration for all methods
    def get_list_enum(self, store_list, id):
        list_name = [list_name for list_name in store_list\
                     if list_name['id'] == id]

        if len(list_name) == 0:
            abort(404)
        return list_name


    def request_json_get(self, store_list):
        store_dict = store_list[0]
        dict_keys = store_dict.keys()   # a list
        for x in dict_keys:
            store_dict[x] = request.json.get(x, store_dict[x])
        return store_dict