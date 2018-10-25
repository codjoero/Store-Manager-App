from flask import Flask, request, jsonify, make_response
from APIs import app
from APIs.views import user_routes, prod_routes, sale_routes

"""Error Handlers 
"""
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized'}), 401)

@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'error': 'Server error'}), 500)

"""Root endpoint
"""
@app.route('/')
def welcome():
    return "Welcome!"

