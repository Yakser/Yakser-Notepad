# from datetime import datetime
# from flask_login import UserMixin
# from sqlalchemy_serializer import SerializerMixin
# from app.data import login_manager
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)
#
#
# def normalize_date(date):
#     date = str(date).split()
#     date[1] = ":".join(date[1].split(':')[:2])
#     date = ' '.join(date)
#     return date
#
#
# def current_date():
#     return normalize_date(datetime.now())
#
#
# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
#     header = db.Column(db.String(255), nullable=False)
#     text = db.Column(db.Text, nullable=True)
#     date = db.Column(db.String(100), nullable=True, default=current_date)
#     favorite = db.Column(db.Boolean, nullable=True)
#     folder_id = db.Column(db.Integer, nullable=False)
#     tags = db.Column(db.String())
#
#     def __repr__(self):
#         return "<Note %r>" % self.id
#
#
# class Folder(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
#     name = db.Column(db.String(255), nullable=False)
#     date = db.Column(db.String(100), nullable=True, default=current_date)
#     acc_users = db.Column(db.String())
#
#     def __repr__(self):
#         return "<Folder %r>" % self.id
#
#
# class AppData(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
#     last_change_date = db.Column(db.String(255), nullable=True, default=current_date)
#
#     def __repr__(self):
#         return "<AppData %r>" % self.id
#
#
# class User(db.Model, UserMixin, SerializerMixin):
#     id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
#     login = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     name = db.Column(db.String(100))
#     surname = db.Column(db.String(100))
#     sex = db.Column(db.String(50))
#     country = db.Column(db.String(100))
#     city = db.Column(db.String(100))
#     phone = db.Column(db.String(100))
#     email = db.Column(db.String(150), unique=True, nullable=False)
#
# # models
# # # Created by Sergey Yaksanov at 27.02.2021
# # Copyright © 2020 Yakser. All rights reserved.
