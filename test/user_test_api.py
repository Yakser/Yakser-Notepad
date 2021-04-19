from requests import get, delete
from requests import get, delete, post

URL = 'http://localhost:5000/api/'


def test_get_users():
    """
    {'users': [{'city': '', 'country': '', 'email': 'iaksanov2044@mail.ru', 'login': 'Yakser', 'name': 'Sergey', 'password': 'pbkdf2:sha256:150000$Tg1RQcoT$5906356b6c79222e2c345286047b3250af5ff2ed650cb6389fdd514f5fc368a8', 'phone': '', 'sex': 'мужской', 'surname': 'Yaksanov'}, {'city': None, 'country': None, 'email': 'sergeyyaksanov@yandex.ru', 'login': 'Test', 'name': 'Sergey', 'password': 'pbkdf2:sha256:150000$JLjL1BNe$0773fe9f5112b2df3e33732a43eb4f610fa01238c12969f68218ae491a809f55', 'phone': None, 'sex': None, 'surname': 'Yaksanov'}]}

    """
    assert tuple(get(f'{URL}/users')
                 .json().keys())[0] == 'users'


def test_get_one_user_correct():
    """
    {'user': {'city': '', 'country': '', 'email': 'iaksanov2044@mail.ru', 'login': 'Yakser', 'modified_date': '2021-04-19 17:39', 'name': 'Sergey', 'password': 'pbkdf2:sha256:150000$Tg1RQcoT$5906356b6c79222e2c345286047b3250af5ff2ed650cb6389fdd514f5fc368a8', 'phone': '', 'sex': 'мужской', 'surname': 'Yaksanov'}}

    """
    assert tuple(get(f'{URL}/users/1')
                 .json().keys())[0] == 'user'


def test_add_user_correct():
    pass


def test_add_user_empty():
    pass


def test_add_user_wrong_json():
    pass


def test_delete_user_correct():
    pass


def test_delete_not_exists_user():
    pass

def test_edit_user_correct():
    pass


# user_test_api
# # Created by Sergey Yaksanov at 24.03.2021
# Copyright © 2020 Yakser. All rights reserved.
