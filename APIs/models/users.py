
from flask import Flask, request, jsonify, abort
from APIs.utilities import Utilities
from database.dbqueries import DbQueries
import datetime
from passlib.hash import pbkdf2_sha256 as sha256

dbq = DbQueries
util = Utilities()

class User:
    """ Class handles user objects """
    def __init__(self, name, username, password, time_stamp, admin):
        self.name = name
        self.username = username
        self.password = password
        self.time_stamp = time_stamp
        self.admin = admin

    def add_user(self):
        """Method adds a user to the database
        """
        dbq.add_user(self.name, self.username, self.password,\
                    self.time_stamp, self.admin)
        return self.name

    def password_hash(self):
        """Method for hashing passwords
        """
        return sha256.hash(self.password)

