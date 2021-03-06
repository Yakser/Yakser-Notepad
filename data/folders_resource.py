from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.folder import Folder
from data.folders_argparser import parser


class FolderResource(Resource):
    """
    Ресурс Folder для одного объекта
    Осуществляет получение и удаление папок
    """

    def get(self, folder_id):
        abort_if_folder_not_found(folder_id)
        session = db_session.create_session()
        folder = session.query(Folder).get(folder_id)
        return jsonify({'folder': folder.to_dict(
            only=('id', 'name', 'date', 'user_id'))})

    def delete(self, folder_id):
        abort_if_folder_not_found(folder_id)
        session = db_session.create_session()
        folder = session.query(Folder).get(folder_id)
        session.delete(folder)
        session.commit()
        return jsonify({'success': 'OK', 'folder_id': folder.id})


class FoldersListResource(Resource):
    """
       Ресурс Folder для списка объектов
       Осуществляет получение и добавление папок
    """

    def get(self):
        session = db_session.create_session()
        folders = session.query(Folder).all()
        return jsonify({'folders': [item.to_dict(
            only=('id', 'name', 'date', 'user_id')) for item
            in folders]})

    def post(self):
        try:

            args = parser.parse_args()
            session = db_session.create_session()
            folder = Folder(
                name=args['name'],
                user_id=args['user_id']
            )
            session.add(folder)
            session.commit()
        except Exception:
            return jsonify({'error': 'Incorrect data'})
        return jsonify({'success': 'OK', 'folder_id': folder.id})


def abort_if_folder_not_found(folder_id):
    """ Вызывает abort(404), если происходит обращение к несуществующей папке"""
    session = db_session.create_session()
    folder = session.query(Folder).get(folder_id)
    if not folder:
        abort(404, message=f"Folder {folder_id} not found")
