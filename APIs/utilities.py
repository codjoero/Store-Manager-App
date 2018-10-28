
from flask import Flask, request, jsonify, abort, make_response
import json


class Utilities():

    # Json input check for all methods
    @classmethod
    def json_check(self, item):
        if not request.json or not item in request.json:
            abort(400)

    @classmethod
    def duplicate_item(self, storage_list, item, _name):
        duplicate = [dict_item for dict_item in storage_list\
                    if dict_item[_name] == item[_name]]
        
        if len(duplicate) != 0:
            return True
        else:
            return False

    # List enumeration for all methods
    @classmethod
    def get_list_enum(self, store_list, _id):
        list_name = [list_name for list_name in store_list\
                     if list_name['_id'] == _id]

        if len(list_name) == 0:
            abort(404)
        return list_name


    # Requests user input in json and updates the list
    @classmethod
    def request_json_get(self, store_list):
        store_dict = store_list[0]
        dict_keys = store_dict.keys()   # a list
        for x in dict_keys:
            store_dict[x] = request.json.get(x, store_dict[x])
        return store_dict


    @classmethod
    def delete_item(self, store_list, list_dict):
        store_list.remove(list_dict[0])
        return True


    @classmethod
    def general_delete(self, store_list, _id):
        list_name = self.get_list_enum(store_list, _id)
        return self.delete_item(store_list, list_name)