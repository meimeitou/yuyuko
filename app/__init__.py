
# from app import models
from flask import Flask, jsonify
from app.model import db
from app.api.router import api
from werkzeug.exceptions import HTTPException, default_exceptions
from config import Config
import logging
from app.socket.terminal import init_terminal

logging.basicConfig(level=logging.INFO)
logging.info(Config.__dict__)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
app = Flask(__name__)
db.init_app(app)
init_terminal(app)

app.config.from_object(Config)
app.register_blueprint(api)
# app.register_blueprint(home)

def make_json_error(err):
    msg = '{}-{}'.format(str(err), getattr(err, 'data', ''))
    response = jsonify(message=msg)
    response.status_code = (
        err.code if isinstance(err, HTTPException) else 500)
    return response

for code in default_exceptions.keys():
    app.register_error_handler(code, make_json_error)
