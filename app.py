import json
import os
import uuid
import logging
from datetime import datetime, timedelta
from functools import wraps

import config
import jwt
from flask import Flask, request, jsonify, make_response, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from ExchangeService import get_exchange_rate_diario_oficial, get_exchange_rate_fixer, get_exchange_rate_xml

()

app = Flask(__name__)
app.config.from_pyfile(os.path.join(".", "app.conf"), silent=False)
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)


limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour", "10 per minute"]
)


def return_json(f):
    @wraps(f)
    def inner(**kwargs):
        return jsonify(f(**kwargs))

    return inner


def authorization(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'x-access-token' in request.headers:
            abort(401)
        token = request.headers['x-access-token']
        try:
            data = jwt.decode(token, os.environ['SECRET_KEY'])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
            if current_user is None:
                abort(401)
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            abort(401)
        return f(*args, **kws)
    return decorated_function


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify user', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    user = Users.query.filter_by(name=auth.username).first()
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
            os.environ['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('could not verify user', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/user', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    result = []
    for user in users:
        user_data = {'public_id': user.public_id, 'name': user.name, 'password': user.password, 'admin': user.admin}
        result.append(user_data)
    return jsonify({'users': result})


@app.route('/')
def hello_world():
    print(config.Config.BANXICO_URL)
    return 'Hello World!'


@app.route('/exchange')
@authorization
@return_json
def exchange_rate():
    data = {'rates': {}}
    data['rates']['fixer'] = get_exchange_rate_fixer('USD', 'MXN')
    data['rates']['diario_oficial'] = get_exchange_rate_diario_oficial()
    data['rates']['banxico'] = get_exchange_rate_xml()
    return data


@app.errorhandler(Exception)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
