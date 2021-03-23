from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_NAME = 'notepad.db'
app.secret_key = "aspddmngmnvcmnjsnuiqrioperjmxvnzxbvoiafwqfoewirn"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notepad.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from app.momentjs import momentjs
from app import views

app.jinja_env.globals['momentjs'] = momentjs
# __init__
# # Created by Sergey Yaksanov at 27.02.2021
# Copyright © 2020 Yakser. All rights reserved.
