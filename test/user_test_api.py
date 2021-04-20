from requests import get, delete, post, put

URL = 'http://localhost:5000/api'


def test_get_users():
    """
    {'users': [{'city': '', 'country': '', 'email': 'iaksanov2044@mail.ru', 'id': 1, 'login': 'Yakser',
     'name': 'Sergey', 'password': '', 'phone': '', 'sex': 'мужской', 'surname': 'Yaksanov'}]}

    """
    assert tuple(get(f'{URL}/users')
                 .json().keys())[0] == 'users'


def test_get_one_user_correct():
    """
    {'user': {'city': '', 'country': '', 'email': 'iaksanov2044@mail.ru', 'id': 1, 'login': 'Yakser',
     'name': 'Sergey', 'password': '', 'phone': '', 'sex': 'мужской', 'surname': 'Yaksanov'}}

    """
    assert tuple(get(f'{URL}/users/1')
                 .json().keys())[0] == 'user'


def test_get_one_user_nonexistent_id():
    """
    {'message': 'User 999 not found'}
    """
    assert get(f'{URL}/users/999').json() == {'message': 'User 999 not found'}


def test_add_user_correct():
    """
    :return:
    """
    resp = post(f'{URL}/users', json={
        'login': 'TestLogin',
        'password': '',
        'name': 'TestName',
        'surname': 'TestSurname',
        'sex': 'male',
        'country': 'Russia',
        'city': 'Saratov',
        'phone': '123',
        'email': 'test@mail.com',
        'modified_date': 'some date'
    }).json()
    assert resp['success'] == 'OK'
    id_ = resp['user_id']
    delete(f'{URL}/users/{id_}')


def test_add_user_already_exists():
    """

    :return:
    """
    id_ = post(f'{URL}/users', json={
        'login': 'TestLogin',
        'password': '',
        'name': 'TestName',
        'surname': 'TestSurname',
        'sex': 'male',
        'country': 'Russia',
        'city': 'Saratov',
        'phone': '123',
        'email': 'test@mail.com',
        'modified_date': 'some date'
    }).json()['user_id']

    resp = post(f'{URL}/users', json={
        'login': 'TestLogin',
        'password': '',
        'name': 'TestName',
        'surname': 'TestSurname',
        'sex': 'male',
        'country': 'Russia',
        'city': 'Saratov',
        'phone': '123',
        'email': 'test@mail.com',
        'modified_date': 'some date'
    }).json()
    delete(f'{URL}/users/{id_}')
    assert resp == {'error': 'User already exists or data is incorrect'}


def test_add_user_wrong_or_empty_json():
    resp = post(f'{URL}/users').json()
    assert resp == {'error': 'User already exists or data is incorrect'}


def test_delete_user_correct():
    id_ = post(f'{URL}/users', json={
        'login': 'TestLogin',
        'password': '',
        'name': 'TestName',
        'surname': 'TestSurname',
        'sex': 'male',
        'country': 'Russia',
        'city': 'Saratov',
        'phone': '123',
        'email': 'test@mail.com',
        'modified_date': 'some date'
    }).json()['user_id']
    assert delete(f'{URL}/users/{id_}').json() == {'success': "OK"}


def test_delete_nonexistent_user():
    id_ = post(f'{URL}/users', json={
        'login': 'TestLogin',
        'password': '',
        'name': 'TestName',
        'surname': 'TestSurname',
        'sex': 'male',
        'country': 'Russia',
        'city': 'Saratov',
        'phone': '123',
        'email': 'test@mail.com',
        'modified_date': 'some date'
    }).json()['user_id']
    delete(f'{URL}/users/{id_}').json()
    assert delete(f'{URL}/users/{id_}').json() == {'message': f"User {id_} not found"}


def test_edit_user_correct():
    id_ = post(f'{URL}/users', json={
        'login': 'TestLogin',
        'password': '',
        'name': 'TestName',
        'surname': 'TestSurname',
        'sex': 'male',
        'country': 'Russia',
        'city': 'Saratov',
        'phone': '123',
        'email': 'test@mail.com',
        'modified_date': 'some date'
    }).json()['user_id']
    assert put(f'{URL}/users/{id_}', json={'name': 'EditedTestName'}).json() == {'success': 'OK'}
    delete(f'{URL}/users/{id_}').json()
# user_test_api
# # Created by Sergey Yaksanov at 24.03.2021
# Copyright © 2020 Yakser. All rights reserved.
