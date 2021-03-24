import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Folder(SqlAlchemyBase, SerializerMixin):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=datetime.datetime.now)
    acc_users = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return "<Folder %r>" % self.id
# folder
# # Created by Sergey Yaksanov at 24.03.2021
# Copyright © 2020 Yakser. All rights reserved.
