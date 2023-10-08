import pytest
import wx
from run_software import *
from dashboard import Dashboard


class Test_dashboard:

    @pytest.fixture
    def my_dashboard(self):
        app = wx.App(0)
        frame = wx.Frame(None)
        return Dashboard(wx.Frame(None), size=(150, 150))

    def test_groupby_single_column(self, my_dashboard):
        out = my_dashboard.groupby_single_column(my_dashboard.df, 'BORO', 'VIOLATION CODE')
        check = isinstance(out, object)
        assert check

    violation_code_dict = [{'04K': 'Rats', '04L': 'Mice', '04M': 'Roach', '04N': 'Flies',
                           '04O': 'Other live animals'}]
    @pytest.mark.parametrize("lst", violation_code_dict)
    def test_groupby_double_column(self, my_dashboard, lst):
        # mapping of violation codes to animals
        filtered_df = my_dashboard.add_new_col(my_dashboard.df, lst, 'VIOLATION CODE', 'ANIMALS').copy()
        filtered_df['INSPECTION DATE'] = pd.to_datetime(filtered_df['INSPECTION DATE'])
        out = my_dashboard.groupby_double_column(filtered_df, 'ANIMALS', 'INSPECTION DATE')
        assert isinstance(out, object)

    def test_get_unique_col_values (self, my_dashboard):
        ani = my_dashboard.get_unique_col_values(my_dashboard.df, 'INSPECTION DATE')
        assert my_dashboard.df['INSPECTION DATE'].unique().all() == ani.all()

