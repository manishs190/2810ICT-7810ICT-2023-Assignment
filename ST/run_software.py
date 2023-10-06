"""
This is the main file to run the software analysis tool.
This file contains :
    Visualize - main class for software
    main - main function of the script
"""
import wx
from homepage import *
from dashboard import *

class Visualize(wx.Frame):
    """
    A class for software initialisation.

    This class contains all the basic methods to run the software

    Attributes
    ----------
        None

    Methods
    -------
        OnHomeTabSelected
            This method will call the home page

        OnDashTabSelected
            This method will call the dashboard page
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the Visualize object.

        Parameters
        ----------
            None
        """
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="Data Analysis Software", pos=wx.DefaultPosition,
                          size= (900, 700), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.Maximize(True)
        self.screen_width, self.screen_height = self.GetSize()

        self.panel = wx.Panel(self)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        # start of main sizer
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        # start of logo section
        self.v_sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.logo = wx.StaticText(self, wx.ID_ANY, u"#Visualise", wx.DefaultPosition, wx.DefaultSize, 5)
        self.logo.SetForegroundColour(wx.Colour(94, 23, 235))
        # font for logo text
        font = wx.Font(16, family=wx.FONTFAMILY_SCRIPT, style=wx.FONTSTYLE_SLANT, weight=100,
                       underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        self.logo.SetFont(font)
        self.v_sizer_1.Add(self.logo, 0, wx.ALL, 20)

        self.v_sizer_1.AddStretchSpacer(1)
        self.main_sizer.Add(self.v_sizer_1, 0, wx.ALL | wx.EXPAND, 5)

        self.line = wx.StaticLine(self, wx.ID_ANY, size = (self.screen_width, 1), style = wx.LI_HORIZONTAL)
        self.main_sizer.Add(self.line)
        # end of logo section

        # start of header section
        self.header = wx.BoxSizer(wx.HORIZONTAL)
        self.header_font = wx.Font(11, family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_SEMIBOLD,
                       underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)

        # add navigation tabs
        self.home_btn = wx.Button(self, label="Home", pos=(30, 20), size=(180, 50))

        # add home tab
        self.home_active_bmp = wx.Bitmap('active_home.png')
        self.home_active_bmp.Rescale(self.home_active_bmp, (35, 35))
        self.home_btn.SetBitmap(self.home_active_bmp)
        self.home_btn.SetBackgroundColour(wx.Colour(94, 23, 235))
        self.home_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.home_btn.Bind(wx.EVT_BUTTON, self.OnHomeTabSelected)
        self.home_btn.SetBitmapPosition(wx.LEFT)
        self.home_btn.SetFont(self.header_font)
        self.header.Add(self.home_btn)

        # call HomePage class
        self.home_tab = HomePage(self)

        # add dashboard tab
        self.dash_inactive_bmp = wx.Bitmap('inactive_dash.png')
        self.dash_inactive_bmp.Rescale(self.dash_inactive_bmp, (35, 35))
        self.dashboard_btn = wx.Button(self, label = "Dashboard", size = (180, 50))
        self.dashboard_btn.SetBackgroundColour(wx.Colour(242, 243, 243))
        self.dashboard_btn.SetForegroundColour(wx.Colour(0, 0, 0))
        self.dashboard_btn.SetBitmap(self.dash_inactive_bmp)
        self.dashboard_btn.SetBitmapPosition(wx.LEFT)
        self.dashboard_btn.SetFont(self.header_font)
        self.dashboard_btn.Bind(wx.EVT_BUTTON, self.OnDashTabSelected)
        self.header.Add(self.dashboard_btn)

        # call Dashboard class
        self.dash_tab = Dashboard(self, (self.screen_width, self.screen_width))

        self.heading = wx.StaticText(self, wx.ID_ANY, u"New York Restaurant Inspection Results", style = wx.ALIGN_RIGHT)
        self.header.AddStretchSpacer(1)
        self.heading.SetFont(self.header_font)
        self.header.Add(self.heading, 0, wx.ALL | wx.ALIGN_LEFT, 20)
        self.main_sizer.Add(self.header, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 15)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.home_tab, -1)
        self.sizer.Add(self.dash_tab, -1)
        self.dash_tab.Hide()
        self.main_sizer.Add(self.sizer, 1, wx.EXPAND)
        # end of header section

        self.footer_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.copyright_text = wx.StaticText(self, wx.ID_ANY, u"Visualise \u00A9 2023", wx.DefaultPosition, wx.DefaultSize, 5)
        self.footer_sizer.Add(self.copyright_text,  0, wx.LEFT|wx.RIGHT|wx.BOTTOM , 20)
        self.main_sizer.Add(self.footer_sizer)

        self.SetAutoLayout(True)
        self.SetSizer(self.main_sizer)
        self.Layout()
        self.Show()

    def OnHomeTabSelected(self, event):
        """
        Calls the function necessary to display the home page.

        Parameters
        ----------
            event
                The event that triggers the function call

        Returns
        -------
            None
        """
        self.home_tab.Show()
        self.home_active_bmp = wx.Bitmap('active_home.png')
        self.home_active_bmp.Rescale(self.home_active_bmp, (35, 35))
        self.home_btn.SetBitmap(self.home_active_bmp)
        self.home_btn.SetBackgroundColour(wx.Colour(94, 23, 235))
        self.home_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.home_btn.SetBitmapPosition(wx.LEFT)

        self.dash_inactive_bmp = wx.Bitmap('inactive_dash.png')
        self.dash_inactive_bmp.Rescale(self.dash_inactive_bmp, (35, 35))
        self.dashboard_btn.SetBackgroundColour(wx.Colour(242, 243, 243))
        self.dashboard_btn.SetForegroundColour(wx.Colour(0, 0, 0))
        self.dashboard_btn.SetBitmap(self.dash_inactive_bmp)
        self.dashboard_btn.SetBitmapPosition(wx.LEFT)

        self.GetSizer().Layout()

    def OnDashTabSelected(self, event):
        """
        Calls the function necessary to display the dashboard page.

        Parameters
        ----------
            event
                The event that triggers the function call
        Returns
        -------
            None
        """
        self.dash_tab.Show()
        self.dash_active_bmp = wx.Bitmap('active_dash.png')
        self.dash_active_bmp.Rescale(self.dash_active_bmp, (35, 35))
        self.dashboard_btn.SetBackgroundColour(wx.Colour(94, 23, 235))
        self.dashboard_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.dashboard_btn.SetBitmap(self.dash_active_bmp)
        self.dashboard_btn.SetBitmapPosition(wx.LEFT)

        self.home_inactive_bmp = wx.Bitmap('inactive_home.png')
        self.home_inactive_bmp.Rescale(self.home_inactive_bmp, (35, 35))
        self.home_btn.SetBitmap(self.home_inactive_bmp)
        self.home_btn.SetBackgroundColour(wx.Colour(242, 243, 243))
        self.home_btn.SetForegroundColour(wx.Colour(0, 0, 0))
        self.home_tab.Hide()
        self.GetSizer().Layout()

if __name__ == "__main__":
    app = wx.App()
    home = Visualize()

    app.MainLoop()