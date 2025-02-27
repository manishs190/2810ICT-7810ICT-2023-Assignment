from run_software import Visualize
import wx
import pytest
from viewdetail import ViewDetailChart

class Test_Visualize:

    @pytest.fixture
    def my_visualize(self):
        app = wx.App(0)
        frame = wx.Frame(None)
        return Visualize()

    @pytest.mark.parametrize("evnt",[wx.EVT_BUTTON])
    def test_OnHomeTabSelected(self, my_visualize,evnt):
        my_visualize.home_btn.Bind(evnt, my_visualize.OnHomeTabSelected)
        assert True

    @pytest.mark.parametrize("evnt", [wx.EVT_BUTTON])
    def test_OnDashTabSelected(self, my_visualize,evnt):
        my_visualize.dashboard_btn.Bind(evnt, my_visualize.OnDashTabSelected)
        assert True


