from common import *
import pytest

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


    def test_filter_data(self):
        filtered_dates_df = None
        filtered_dates_df = filter_data('INSPECTION DATE', load_file(r"DOHMH_New_York_City_Restaurant_Inspection_Results.csv"), datetime.datetime(2017, 1, 1), datetime.datetime(2017, 2, 15))
        assert not filtered_dates_df.empty and isinstance(filtered_dates_df, object)

