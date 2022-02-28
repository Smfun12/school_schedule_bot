import numpy as np
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from constant import SCOPE, JSON_ROUTE, MAIN_TABLE


# open main table
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_ROUTE, SCOPE)
client = gspread.authorize(credentials)
table = client.open(MAIN_TABLE)


class Frame:
    def __init__(self):
        self.sheet = table.worksheet('data')
        data = np.array(self.sheet.get_all_values())
        records = data[1:]
        columns = data[0]
        self.df = pd.DataFrame(records, columns=columns)
        self.users_num = self.df.shape[0] - (self.df['telegram_id'] == '').sum()


frame = Frame()


def get_login_password(telegram_id):
    """
    Takes telegram id of the user and returns their login and password
    Registers new users
    :param telegram_id: telegram id of the user
    :return: login, password
    """
    user_idx = frame.df[frame.df['telegram_id'] == str(telegram_id)].index
    if user_idx.shape[0] == 0:
        __register_user(telegram_id)
        user_idx = [frame.users_num]
    user = frame.df.iloc[user_idx].to_numpy()[0]
    return user[0], user[1]


def __register_user(telegram_id):
    __update_cell(frame.users_num, 2, telegram_id)


def __is_registered(telegram_id):
    user = frame.df[frame.df['telegram_id'] == str(telegram_id)]
    if user.shape[0] == 0:
        return False
    return True


def __get_user_row(telegram_id):
    return frame.df[frame.df['telegram_id'] == str(telegram_id)].index[0]


def __update_cell(i, j, value):
    y, x = __sheet_coords(i, j)
    frame.sheet.update_cell(y, x, str(value))
    frame.df.iloc[i, j] = str(value)


def __sheet_coords(i, j):
    return i+2, j+1

