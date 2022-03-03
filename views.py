from flask import request, jsonify, make_response
from functools import wraps
from flask.views import MethodView
from app import app, db, AdvertisementModel, UserModel
from jsonschema import validate, ValidationError
from schema import CREATE_USER, CREATE_ADV
# Функция для хэширования и проверки, поставляемые вместе с Flask
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
import uuid


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.current_user = UserModel.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)
    return decorator


class UserView(MethodView):

    def post(self):

        if not self.on_valid(CREATE_USER) == None:
            return self.on_valid(CREATE_USER)

        request.json['password'] = generate_password_hash(request.json['password'])
        request.json['public_id'] = str(uuid.uuid4())

        new_user = UserModel(**request.json)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            {
                'id': new_user.id,
                'user': f'{new_user.first_name} {new_user.last_name}',
                'message': 'registered successfully'
            }
        )

    @token_required
    def delete(self):
        user = request.current_user
        db.session.delete(user)
        db.session.commit()
        return jsonify(
            {
                'message': 'user was deleted'
            }
        )

    @token_required
    def put(self):
        user = request.current_user
        data = request.get_json()
        for item, value in data.items():
            if item == 'email':
                user.email = value
            if item == 'first_name':
                user.first_name = value
            if item == 'last_name':
                user.last_name = value
            if item == 'password':
                user.password = generate_password_hash(value)
        db.session.add(user)
        db.session.commit()
        return jsonify(
            {
                'message': 'user was changed'
            }
        )

    def on_valid(self, schema_variable):
        try:
            validate(request.json, schema_variable)
        except ValidationError as err:
            response = jsonify({
                'error': 'not valid',
                'description': err.message
            })
            response.status_code = 400
            return response



class AdvertisementView(MethodView):

    @token_required
    def get(self, id):
        adv = AdvertisementModel.query.get(id)
        if adv == None:
            response = jsonify({
                'message': 'There is not such advertisement in database'
            })
            response.status_code = 400
            return response
        return jsonify(
            {
            'id': adv.id,
            'title': adv.title,
            'description': adv.description,
            'publish_date': adv.publish_date,
            'owner_id': adv.owner_id
            }
        )

    @token_required
    def post(self):

        if not UserView.on_valid(self, CREATE_ADV) == None:
            return UserView.on_valid(self, CREATE_ADV)

        request.json['owner_id'] = request.current_user.id

        new_adv = AdvertisementModel(**request.json)
        db.session.add(new_adv)
        db.session.commit()
        return jsonify(
            {
                'id': new_adv.id,
                'advertisement': new_adv.title,
                'status': 'created'
            }
        )

    @token_required
    def delete(self, id):
        adv = AdvertisementModel.query.filter_by(owner_id=request.current_user.id, id=id).first()
        if adv == None:
            response = jsonify({
                'message': 'You have not such advertisement'
            })
            response.status_code = 400
            return response
        db.session.delete(adv)
        db.session.commit()
        return jsonify(
            {
                'message': 'advertisement was deleted'
            }
        )

    @token_required
    def put(self, id):
        adv = AdvertisementModel.query.filter_by(owner_id=request.current_user.id, id=id).first()
        if adv == None:
            response = jsonify({
                'message': 'You have not such advertisement'
            })
            response.status_code = 400
            return response
        data = request.get_json()
        for item, value in data.items():
            if item == 'title':
                adv.title = value
            if item == 'description':
                adv.description = value
        db.session.add(adv)
        db.session.commit()
        return jsonify(
            {
                'message': 'advertisement was changed'
            }
        )


@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    user = UserModel.query.filter_by(user_login=auth.username).first()
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
            app.config['SECRET_KEY'], "HS256")

        return jsonify({'token': token})

    return make_response('could not verify', 401, {'Authentication': '"login required"'})


# Альтернативный способ роута. GET идет как default
# @app.route('/advertisements', methods=['GET'])
def get_list():
    advs = AdvertisementModel.query.all()
    return {'Advertisements': list({'id': x.id,
                                    'title': x.title,
                                    'description': x.description,
                                    'publish_date': x.publish_date,
                                    'owner_id': x.owner} for x in advs)}



app.add_url_rule('/user', view_func=UserView.as_view('create_user'), methods=['POST'])
app.add_url_rule('/user/<int:id>', view_func=UserView.as_view('user'),
                 methods=['GET', 'DELETE', 'PUT'])

app.add_url_rule('/advs', view_func=get_list, methods=['GET'])
app.add_url_rule('/adv', view_func=AdvertisementView.as_view('create_adv'), methods=['POST'])
app.add_url_rule('/adv/<int:id>', view_func=AdvertisementView.as_view('adv'),
                 methods=['GET', 'DELETE', 'PUT'])