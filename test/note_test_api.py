from requests import get, delete, put

from requests import get, delete, post

URL = 'http://localhost:5000/api'


def test_get_notes():
    assert tuple(get(f'{URL}/notes')
                 .json().keys())[0] == 'notes'


def test_get_one_note_correct():
    assert tuple(get(f'{URL}/notes/1')
                 .json().keys())[0] == 'note'


def test_get_one_note_nonexistent_id():
    assert get(f'{URL}/notes/999').json() == {'message': 'Note 999 not found'}


def test_get_one_note_wrong_type_of_id():
    assert get(f'{URL}/notes/abcd').json() == {'error': 'Not found'}


def test_add_note_correct():
    resp = post(f'{URL}/notes', json={'header': "TestHeader",
                                      'text': 'TestText', 'folder_id': '0', 'tags': ''}).json()
    id_ = resp['note_id']
    delete(f'{URL}/notes/{id_}')
    assert resp['success'] == 'OK'


def test_add_note_wrong_or_empty_json():
    resp = post(f'{URL}/notes', json={}).json()
    assert resp == {'error': 'Incorrect data'}


def test_delete_note_correct():
    id_ = post(f'{URL}/notes', json={'header': "TestHeader",
                                     'text': 'TestText', 'folder_id': '0', 'tags': ''}).json()['note_id']

    assert delete(f'{URL}/notes/{id_}').json()['success'] == 'OK'


def test_delete_nonexistent_note():
    assert delete(f'{URL}/notes/999').json() == {'message': 'Note 999 not found'}


def test_edit_note_correct():
    id_ = post(f'{URL}/notes', json={'header': "TestHeader",
                                     'text': 'TestText', 'folder_id': '0', 'tags': ''}).json()['note_id']
    assert put(f'{URL}/notes/{id_}', json={'header': "EditedTestHeader"}).json() == {'success': "OK"}
    delete(f'{URL}/notes/{id_}')
