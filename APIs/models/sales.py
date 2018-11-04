from flask import Flask, request, jsonify, abort
import datetime
from APIs.utilities import Utilities

util = Utilities()

class Sales:
    """ Class handles sales views """
    sales = []

    def __init__(self, prod_name, category, stock, price):
        self.prod_name = prod_name
        self.category = category
        self.stock = stock
        self.price = price
