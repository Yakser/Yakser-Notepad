import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import login_manager
from .db_session import SqlAlchemyBase


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    sex = sqlalchemy.Column(sqlalchemy.String)
    country = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String)
    phone = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    # modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
    #                                   default=datetime.datetime.now)

    # todo relation

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"<User> {self.id} {self.surname} {self.name}"

# users
# # Created by Sergey Yaksanov at 01.03.2021
# Copyright © 2020 Yakser. All rights reserved.
