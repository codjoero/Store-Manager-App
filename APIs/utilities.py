
from flask import Flask, request, jsonify, abort, make_response
import json
import re


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

class UserValidation():
    """Class validates all user inputs
    """
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def valid_name(self):
        """Method validates user's name,
        Returns True for valid, False otherwise
        """
        numbers = re.search(r"[0-9]", self.name)
        if numbers:
            return False
        if not self.name or isinstance(self.name, int) or\
            not isinstance(self.name, str):
            return False
        else:
            return True

    def valid_username(self):
        """Method validates username,
        Returns True for valid, False otherwise
        """
        numbers = re.search(r"[0-9]", self.username)
        if numbers:
            return False
        if isinstance(self.username, int):
            return False
        if ' ' in self.username or not self.username or\
            self.username.isspace() or\
            not isinstance(self.username, str):
            return False
        else:
            return True 

    def valid_password(self):
        """Method validates user's password,
        Returns True for valid, False otherwise
        """
        numbers = re.search(r"[0-9]", self.password)
        lower_case = re.search(r"[a-z]", self.password)
        upper_case = re.search(r"[A-Z]", self.password)

        if ' ' in self.password or\
            not all((numbers, lower_case, upper_case)) or\
            not len(self.password) > 6:
            return False
        else:
            return True

class ProductValidation():
    """Class validates all product inputs
    """
    def __init__(self, *args):
        self.prod_name = args[0]
        self.category = args[1]
        self.stock = args[2]
        self.price = args[3]

    def valid_product(self):
        """Method to validate all product attributes
        """
        invalid_name = re.search(r"[0-9]", self.prod_name)
        invalid_category = re.search(r"[0-9]", self.category)
        if invalid_name or invalid_category:
            return False
        if not self.prod_name or not self.category or\
            not self.stock or not self.price or\
            self.prod_name.isspace():
            return False
        else:
            return True

    def valid_prod_fields(self):
        """Method to validate each field of product
        """
        if self.prod_name and ' ' in self.prod_name or\
            self.category and ' ' in self.category or\
            self.stock and not isinstance(self.stock, int) or\
            self.price and not isinstance(self.price, int):
            return False
        else:
            return True

class SaleValidation():
    """Class validates all sale records inputs"""

    def __init__(self, products):
        self.products = products

    def valid_sale(self):
        for product in self.products:
            if not product['prod_name'] or\
                not product['quantity'] or\
                product['prod_name'].isspace():
                return False
        return True
    
    def valid_types(self):
        for product in self.products:
            if not isinstance(product['prod_name'], str) or\
                not isinstance(product['quantity'], int):
                return False
        return True


