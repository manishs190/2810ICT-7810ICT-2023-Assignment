import pytest
from homepage import HomePage
import wx
import pandas as pd
from common import load_file
from run_software import Visualize


class Test_homepage:

    @pytest.fixture
    def my_homepage(self):
        #obj = my_Visualize()
        app = wx.App(0)
        frame = wx.Frame(None)
        return HomePage(wx.Frame(None))

    excluded_col_list =[['CAMIS', 'BUILDING', 'ZIPCODE', 'PHONE', 'INSPECTION DATE', 'SCORE', 'GRADE',
    'GRADE DATE', 'RECORD DATE'], [], ['NOT THERE']]
    @pytest.mark.parametrize("excl", excluded_col_list)
    def test_get_col_choices(self, my_homepage, excl):
        try:
            df = pd.read_csv("DOHMH_New_York_City_Restaurant_Inspection_Results.csv")

            choices = my_homepage.get_col_choices(excl, df.columns)
            ls = []
            for x in df.columns:
                if x not in excl:
                    ls.append(x)
            print(ls)
            output =  choices.sort() == ls.sort()
        except:
            output = False
        assert output

    def test_OnExportToCSV(self, my_homepage):
        filter_sizer = wx.BoxSizer(wx.HORIZONTAL)
        my_homepage.export_btn.Bind(wx.EVT_BUTTON, my_homepage.OnExportToCSV)
        out = load_file("output.csv")
        assert isinstance(out, object)





