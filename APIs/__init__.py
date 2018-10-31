from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'my-my-my-you-cant-touch-this'
jwt = JWTManager(app)

import APIs.views