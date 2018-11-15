from flask import Flask, jsonify
from APIs.utilities import Utilities
from database.dbqueries import DbQueries
import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import get_jti

dbq = DbQueries()
util = Utilities()

class User:
    """ Class handles user objects """

    def __init__(self, name, username, password, role):
        self.name = name
        self.username = username
        self.password = password
        self.role = role

    def add_user(self):
        """Method adds a user to the database
        """
        dbq.add_user(self.name, self.username, self.password, self.role)
        return self.name

    def password_hash(self):
        """Method for hashing passwords
        """
        return sha256.hash(self.password)

    @staticmethod
    def password_verification(username, password):
        """Method to verify input password with
        corresponding username
        """
        user = User.query_item('users', 'username', username)
        if not sha256.verify(password, user[3]):
            return False
        else:
            return True
         
    @staticmethod
    def query_item(table, column, value):
        """Method to fetch a specific item
        Returns a row of the item, and false otherwise
        """
        item = dbq.query_item(table, column, value)
        if not item:
            return False
        else:
            return item

    @staticmethod
    def logout(tk_jti):
        """Method to check jti in blacklisted_tokens
       
        """
        if User.query_item('blacklisted_tokens', 'tk_jti', tk_jti):
            return jsonify({
                'message': 'You are already logged out!'
            }), 404
        try:
            dbq.add_jti(tk_jti)
            return jsonify({
                'message': 'You are successfully logged out!'
            }), 200
        except Exception as err:
            return jsonify({
                'message': {err}
            }), 409

    @staticmethod
    def valid_token(header):
        """Method to check for validity of a token
        Checks blacklisted_tokens database
        returns: True for valid token, False otherwise
        """
        auth_header = header.get('Authorization')
        try:
            auth_token = auth_header.split(" ")[1]
            tk_jti = get_jti(auth_token)
            if User.query_item('blacklisted_tokens', 'tk_jti', tk_jti):
                return False
            return True
        except Exception:
            return False