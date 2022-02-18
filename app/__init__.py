
# from app import models
from flask import Flask, jsonify
from flask_bootstrap import Bootstrap5
from app.model import db
from app.api import api
from app.home.home import app as home
from werkzeug.exceptions import HTTPException, default_exceptions
from config import Config
import logging
from flask_wtf import  CSRFProtect

logging.basicConfig(level=logging.INFO)
logging.info(Config.__dict__)
app = Flask(__name__, static_folder="app/static", template_folder='app/templates')
bootstrap = Bootstrap5(app)
db.init_app(app)
csrf = CSRFProtect(app)

app.config.from_object(Config)
app.register_blueprint(api)
app.register_blueprint(home)

def make_json_error(err):
    msg = '{}-{}'.format(str(err), getattr(err, 'data', ''))
    response = jsonify(message=msg)
    response.status_code = (
        err.code if isinstance(err, HTTPException) else 500)
    return response

for code in default_exceptions.keys():
    app.register_error_handler(code, make_json_error)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    draft = db.Column(db.Boolean, default=False, nullable=False)
    create_time = db.Column(db.Integer, nullable=False, unique=True)

@app.before_first_request
def before_first_request_func():
    db.drop_all()
    db.create_all()
    for i in range(20):
        m = Message(
            text=f'Test message {i+1}',
            author=f'Author {i+1}',
            category=f'Category {i+1}',
            create_time=4321*(i+1)
        )
        if i % 4:
            m.draft = True
        db.session.add(m)
    db.session.commit()
