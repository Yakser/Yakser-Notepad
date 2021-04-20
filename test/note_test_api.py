from requests import get, delete

from requests import get, delete, post

URL = 'http://localhost:5000/api'


def test_get_notes_correct():
    assert tuple(get(f'{URL}/notes')
                 .json().keys())[0] == 'notes'


def test_get_one_note_correct():
    assert tuple(get(f'{URL}/notes/1')
                 .json().keys())[0] == 'note'


def test_get_one_note_nonexistent_id():
    assert get(f'{URL}/notes/999').json() == {'message': 'Note 999 not found'}


def test_get_one_note_wrong_type_of_id():
    assert get(f'{URL}/notes/abcd').json() == {'error': 'Not found'}

# note_test_api
# # Created by Sergey Yaksanov at 25.03.2021
# Copyright © 2020 Yakser. All rights reserved.
