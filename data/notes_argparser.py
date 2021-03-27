from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('header', required=True)
parser.add_argument('text', required=True)
parser.add_argument('favorite', required=True)
parser.add_argument('folder_id', required=True)
parser.add_argument('tags', required=True)


# notes_argparser
# # Created by Sergey Yaksanov at 25.03.2021
# Copyright © 2020 Yakser. All rights reserved.
