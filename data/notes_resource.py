from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.note import Note
from data.notes_argparser import parser, edit_parser


class NoteResource(Resource):
    def get(self, note_id):
        abort_if_note_not_found(note_id)
        session = db_session.create_session()
        note = session.query(Note).get(note_id)
        return jsonify({'note': note.to_dict(
            only=('id', 'header', 'text', 'folder_id', 'tags'))})

    def put(self, note_id):
        abort_if_note_not_found(note_id)
        try:
            args = edit_parser.parse_args()
            session = db_session.create_session()
            note = session.query(Note).get(note_id)
            note.header = args.get('header', note.header)
            note.text = args.get('text', note.text)
            note.tags = args.get('tags', note.tags)
            note.folder_id = args.get('folder_id', note.folder_id)
            session.commit()
        except Exception:
            return jsonify({'error': 'incorrect data'})
        return jsonify({'success': 'OK'})

    def delete(self, note_id):
        abort_if_note_not_found(note_id)
        session = db_session.create_session()
        note = session.query(Note).get(note_id)
        session.delete(note)
        session.commit()
        return jsonify({'success': 'OK', 'note_id': note.id})


class NotesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        notes = session.query(Note).all()
        return jsonify({'notes': [item.to_dict(
            only=('id', 'header', 'text', 'folder_id', 'tags')) for item
            in notes]})

    def post(self):
        try:

            args = parser.parse_args()
            session = db_session.create_session()
            note = Note(
                header=args['header'],
                text=args['text'],
                folder_id=args['folder_id'],
                tags=args['tags'],
            )
            session.add(note)
            session.commit()
        except Exception:
            return jsonify({'error': 'Incorrect data'})
        return jsonify({'success': 'OK', 'note_id': note.id})


def abort_if_note_not_found(note_id):
    session = db_session.create_session()
    note = session.query(Note).get(note_id)
    if not note:
        abort(404, message=f"Note {note_id} not found")

# note_resource
# # Created by Sergey Yaksanov at 24.03.2021
# Copyright © 2020 Yakser. All rights reserved.
