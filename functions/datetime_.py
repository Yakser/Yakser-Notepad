from datetime import datetime


def normalize_date(date):
    date = str(date).split()
    date[1] = ":".join(date[1].split(':')[:2])
    date = ' '.join(date)
    return date


def current_date():
    return normalize_date(datetime.now())


# datetime_
# # Created by Sergey Yaksanov at 27.03.2021
# Copyright © 2020 Yakser. All rights reserved.
