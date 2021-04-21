from flask_restful import reqparse
# парсер аргументов для Note
parser = reqparse.RequestParser()
parser.add_argument('header', required=True)
parser.add_argument('text', required=True)
parser.add_argument('folder_id', required=True)
parser.add_argument('tags', required=True)

# парсер аргументов для Note - редактирование
edit_parser = reqparse.RequestParser()
edit_parser.add_argument('header', required=False)
edit_parser.add_argument('text', required=False)
edit_parser.add_argument('folder_id', required=False)
edit_parser.add_argument('tags', required=False)


# notes_argparser
# # Created by Sergey Yaksanov at 25.03.2021
# Copyright © 2020 Yakser. All rights reserved.
