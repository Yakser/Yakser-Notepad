from datetime import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from functions.datetime_ import current_date
from .db_session import SqlAlchemyBase


class Folder(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'folder'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=current_date)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("user.id"))

    user = orm.relation('User')

    notes = orm.relation("Note", back_populates='folder')

    def __repr__(self):
        return "<Folder %r>" % self.id
# folder
# # Created by Sergey Yaksanov at 24.03.2021
# Copyright © 2020 Yakser. All rights reserved.
