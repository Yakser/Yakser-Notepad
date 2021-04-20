from requests import get, delete, post

URL = 'http://localhost:5000/api/'


def test_get_one_folder_correct():
    """
        {'folder':
         {'date': '2021-03-27 00:11', 'id': 1, 'name': 'folder', 'user_id': 1}}
    """
    assert tuple(get(f'{URL}/folders/1')
                 .json().keys())[0] == 'folder'


def test_get_one_folder_wrong_id():
    """
        corr: {'message': 'Folder 999 not found'}
    """
    assert get(f'{URL}/folders/999').json() == \
           {'message': 'Folder 999 not found'}


def test_get_one_folder_wrong_type_of_id():
    """
        corr: {'error': 'Not found'}
    """
    assert get(f'{URL}/folders/abcd').json() == \
           {'error': 'Not found'}


def test_get_folders():
    """ corr: {'folders'
     [{'date': '2021-03-27 00:11', 'id': 1, 'name': 'folder', 'user_id': 1}}]}
    """
    assert tuple(get(f'{URL}/folders')
                 .json().keys())[0] == 'folders'


# def test_delete_exists_folder():
#     """
#     corr: {'success': 'OK'}
#     """
#     random_name = 'jahdjkasd'
#     post(f'{URL}/api/folders', json={'name': random_name, 'user_id': '999'})
#     session = db_session.create_session()
#     id_ = session.query(Folder).filter(Folder.name == random_name).first().id
#     session.close()
#     assert tuple(delete(f'{URL}/api/folders/{id_}')
#                  .json()) == {'success': 'OK'}


def test_delete_nonexistent_folder():
    """
    corr: {'message': 'Folder 999 not found'}
    """
    assert delete(f'{URL}/folders/999').json() == {'message': 'Folder 999 not found'}


def test_add_folder_correct():
    """
    corr: {'error': 'Not found'}
    """
    resp = post(f'{URL}/folders',
                json={'name': 'TestName', 'user_id': '0'}).json()

    assert resp['success'] == 'OK'
    id_ = resp['folder_id']
    delete(f'{URL}/folders/{id_}')


def test_add_folder_empty():
    """
    corr: {'message': {'name': 'Missing required parameter in the JSON body or the post body or the query string'}}

    """
    resp = post(f'{URL}/folders').json()
    assert resp['message'] == {'name': 'Missing required parameter in'
                                       ' the JSON body or the post body or the query string'}

#
# test_folder_api
# # Created by Sergey Yaksanov at 25.03.2021
# Copyright © 2020 Yakser. All rights reserved.
