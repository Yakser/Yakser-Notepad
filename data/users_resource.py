from flask import jsonify
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash

from data import db_session
from data.user import User
from data.users_argparser import parser


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('login', 'password', 'name', 'surname',
                  'sex', 'country', 'city', 'phone', 'email', 'modified_date'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('login', 'password', 'name', 'surname',
                  'sex', 'country', 'city', 'phone', 'email')) for item
            in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            login=args['login'],
            password=generate_password_hash(args['password']),
            name=args['name'],
            surname=args['surname'],
            sex=args['sex'],
            country=args['country'],
            city=args['city'],
            phone=args['phone'],
            email=args['email']

        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")

# users_resource
# # Created by Sergey Yaksanov at 24.03.2021
# Copyright © 2020 Yakser. All rights reserved.
