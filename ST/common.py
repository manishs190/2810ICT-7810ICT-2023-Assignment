import pandas as pd
import wx
import wx.adv
import datetime

def load_file():
    df = pd.read_csv(r"DOHMH_New_York_City_Restaurant_Inspection_Results.csv")

    return df

def set_from_date(parent):
    from_date_field = wx.adv.DatePickerCtrl(parent, style=wx.adv.DP_DROPDOWN)
    from_date_field.SetRange(datetime.datetime(1900, 1, 1), datetime.datetime(2017, 12, 31))

    return from_date_field

