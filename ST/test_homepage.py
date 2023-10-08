import pytest
from homepage import HomePage
from homepage import DataTable
import wx
import pandas as pd
from common import load_file

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

    lst = [wx.EVT_BUTTON]
    @pytest.mark.parametrize("excl", lst)
    def test_OnExportToCSV(self, my_homepage, excl):
        my_homepage.export_btn.Bind(excl, my_homepage.OnExportToCSV)
        out = load_file("output.csv")
        assert isinstance(out, object)

    col_list = [('BORO',['CAMIS', 'BUILDING', 'ZIPCODE', 'PHONE', 'INSPECTION DATE', 'SCORE', 'GRADE',
                 'GRADE DATE', 'RECORD DATE', 'BORO']), ('NOT THERE',['CAMIS', 'BUILDING', 'ZIPCODE', 'PHONE', 'INSPECTION DATE', 'SCORE', 'GRADE',
                 'GRADE DATE', 'RECORD DATE'])]

    @pytest.mark.parametrize("val, colList", col_list)
    def test_check_column_name(self, my_homepage, val, colList):
        out = False
        if val in colList:
            out = my_homepage.check_column_name(val, colList)
        else:
            out = True
        assert out

    @pytest.mark.parametrize("dataFrame", [load_file("output.csv")])
    def test_SetDataTable(self,my_homepage, dataFrame):
        my_homepage.SetDataTable(dataFrame)
        assert True

    @pytest.fixture
    def my_DataTable(self):
        return DataTable(load_file("output.csv"))

    def test_GetNumberRows(self, my_DataTable):
        rows = my_DataTable.GetNumberRows()
        assert rows > 0 and rows == 399918

    def test_GetNumberCols(self, my_DataTable):
        cols = my_DataTable.GetNumberCols()
        assert cols > 0 and cols == 18

    @pytest.mark.parametrize("row, col", [(23, 16)])
    def test_GetValue(self, my_DataTable, row, col):
        da = my_DataTable.GetValue(row, col)
        assert da != None and isinstance(da, object)

    @pytest.mark.parametrize("col", [0])
    def test_GetColLabelValue(self,my_DataTable, col):
        dat = my_DataTable.GetColLabelValue(col)
        assert dat !=None and dat == 'CAMIS'

    @pytest.mark.parametrize("col", [16])
    def test_GetAttr(self, my_DataTable, col):
        attr = my_DataTable.GetColLabelValue(col)
        assert attr !=None and attr == 'RECORD DATE'





