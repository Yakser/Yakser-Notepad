from datetime import datetime


def normalize_date(date):
    """
    Приводит дату к читаемому виду
    """
    date = str(date).split()
    date[1] = ":".join(date[1].split(':')[:2])
    date = ' '.join(date)
    return date


def current_date():
    """
    Возвращает текущую нормализованную дату
    """
    return normalize_date(datetime.now())

# datetime_
# # Created by Sergey Yaksanov at 27.03.2021
# Copyright © 2020 Yakser. All rights reserved.
