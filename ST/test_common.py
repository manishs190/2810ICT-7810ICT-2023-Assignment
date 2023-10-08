from common import *
import wx
from homepage import HomePage
import wx
import pytest
import datetime
class TestCommon:

    file_names = [' ', r"DOHMH_New_York_City_Restaurant_Inspection_Results.csv",'wrong_file']
    @pytest.mark.parametrize("fileStr",file_names)
    def test_load_file(self, fileStr):
        try:
            output = load_file(fileStr)
            flag_right = isinstance(output, object) or output=='IO_error'
            error = not flag_right
        except:
            error = True
        assert not error

    def test_check_date_range(self):
        dateLst = get_date_range()
        assert dateLst[0] < dateLst[1] and check_date_range(dateLst)




