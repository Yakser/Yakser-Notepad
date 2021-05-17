from flask_restful import reqparse

# парсер аргументов для Folder
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('user_id', required=True)
