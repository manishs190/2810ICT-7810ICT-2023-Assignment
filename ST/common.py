import pandas as pd
import wx
import wx.adv
import datetime
import os


def load_file(filename):
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        return df
    else:
        return 'IO_error'

def get_date_range():
    date1 = datetime.datetime(1900, 1, 1)
    date2 = datetime.datetime(2017, 12, 31)

    return [date1, date2]

def check_date_range(date):

    is_valid = False
    if date[0] < date[1]:
        is_valid = True
    print(is_valid)
    return is_valid
