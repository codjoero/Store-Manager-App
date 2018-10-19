
from flask import Flask, request, jsonify, abort, make_response
import json

class Utilities():

    def json_check(self, item):
        if not request.json or not item in request.json:
            abort(400)