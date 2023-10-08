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

    return is_valid

def filter_data(col_name, data, min_date, max_date):
    # the pandas series is converted to datetime
    datetime_converted_1 = pd.to_datetime(data[col_name], infer_datetime_format=True)
    filtered_df = data[datetime_converted_1 >= datetime.datetime(min_date.year, min_date.month + 1, min_date.day)]

    datetime_converted_2 = pd.to_datetime(filtered_df[col_name], infer_datetime_format=True)
    filtered_df = filtered_df[datetime_converted_2 <= datetime.datetime(max_date.year, max_date.month + 1, max_date.day)]

    return filtered_df