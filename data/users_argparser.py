from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('login', required=True)
parser.add_argument('password', required=True)
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('sex', required=True)
parser.add_argument('country', required=True)
parser.add_argument('city', required=True)
parser.add_argument('phone', required=True)
parser.add_argument('email', required=True)
parser.add_argument('modified_date', required=True)

edit_parser = reqparse.RequestParser()
edit_parser.add_argument('name', required=False)
edit_parser.add_argument('surname', required=False)
edit_parser.add_argument('sex', required=False)
edit_parser.add_argument('country', required=False)
edit_parser.add_argument('city', required=False)
edit_parser.add_argument('phone', required=False)


# users_argparser
# # Created by Sergey Yaksanov at 24.03.2021
# Copyright © 2020 Yakser. All rights reserved.
