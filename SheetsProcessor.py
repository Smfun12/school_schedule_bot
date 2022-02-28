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
        self.sheet = table.worksheet('sheet_one')
        data = np.array(self.sheet.get_all_values())
        records = data[1:]
        columns = data[0]
        self.df = pd.DataFrame(records, columns=columns)


frame = Frame()


def get_login_password(telegram_id):
    user = frame.df[frame.df['telegram_id'] == str(telegram_id)]
    if user.shape[0] == 0:
        register_user(telegram_id)


def register_user(telegram_id):
    pass


def is_registered(telegram_id):
    return False


def __get_user_row(telegram_id):
    pass


def __update_cell(i, j, value):
    pass


def __sheet_coords(i, j):
    return i+2, j+1