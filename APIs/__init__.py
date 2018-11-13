from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'my-my-my-you-cant-touch-this'
jwt = JWTManager(app)
CORS(app)

import APIs.views