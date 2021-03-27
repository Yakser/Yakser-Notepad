from flask_login import current_user

from data import db_session
from data.user import User
from functions.datetime_ import current_date


def update_last_change_date():
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    user.modified_date = current_date()
    session.commit()

# update_last_change_date
# # Created by Sergey Yaksanov at 27.03.2021
# Copyright © 2020 Yakser. All rights reserved.
