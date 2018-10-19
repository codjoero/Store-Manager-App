from flask import Flask
from APIs.app import app


if __name__ == '__main__':
    app.run(debug=True)