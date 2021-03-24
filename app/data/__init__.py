from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from app.data import db_session

app = Flask(__name__)
api = Api(app)
# DB_NAME = 'notepad.db'
app.secret_key = "aspddmngmnvcmnjsnuiqrioperjmxvnzxbvoiafwqfoewirn"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notepad.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)

from app.data.momentjs import momentjs
from app.data import users_resource

app.jinja_env.globals['momentjs'] = momentjs
db_session.global_init("C:\\Python1\\Python37\\Projects\\Notepaddy\\app\db\\notepad.db")

# __init__
# # Created by Sergey Yaksanov at 24.02.2021
# Copyright © 2020 Yakser. All rights reserved.
