from flask_login import current_user

from app import db
from app.models import AppData, Folder, Note, current_date

def update_last_change_date():
    AppData.query.first().last_change_date = current_date()
    db.session.commit()
def get_accessible_folders():
    try:
        acc_folders = Folder.query.filter(Folder.acc_users.contains(current_user.id)).all()
        return acc_folders
    except AttributeError:
        return []
def get_folder_id(name, query_by_note_id=False):
    if not query_by_note_id:
        founded_folder = Folder.query.filter(Folder.name == name.lower()).first()
        if founded_folder:
            return founded_folder.id
    else:
        founded_note = Note.query.filter(Note.id == name).first()
        if founded_note:
            return founded_note.folder_id
def get_folder_name(folder_id):
    founded_folder = Folder.query.filter(Folder.id == folder_id).first()
    if founded_folder:
        return founded_folder.name
    return ''

# funcs
# # Created by Sergey Yaksanov at 27.02.2021
# Copyright © 2020 Yakser. All rights reserved.
