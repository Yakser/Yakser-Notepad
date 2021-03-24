import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Note(SqlAlchemyBase, SerializerMixin):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    header = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=datetime.datetime.now)
    favorite = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    folder_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    tags = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return "<Note %r>" % self.id

# note
# # Created by Sergey Yaksanov at 24.03.2021
# Copyright © 2020 Yakser. All rights reserved.
