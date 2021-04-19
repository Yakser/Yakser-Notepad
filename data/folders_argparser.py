from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('user_id', required=True)


# folders_argparser
# # Created by Sergey Yaksanov at 25.03.2021
# Copyright © 2020 Yakser. All rights reserved.
