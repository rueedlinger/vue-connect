from flask import Flask
from flask_cors import CORS
from flask import g
import logging

logging.basicConfig(level=logging.INFO)


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


from app import routes
