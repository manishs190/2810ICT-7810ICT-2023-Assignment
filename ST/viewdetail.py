"""
This file contains classes and methods for detailed plot display.
This file contains :
    ViewDetailChart - main class for detailed plot display in a new window

Reference: https://wiki.wxpython.org/How%20to%20use%20Matplotlib%20-%20Part%201%20%28Phoenix%29
"""
import wx
import pandas as pd
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import matplotlib.pyplot as plt

# data file used for analysis
df = pd.read_csv(r"DOHMH_New_York_City_Restaurant_Inspection_Results.csv")

class ViewDetailChart(wx.Frame):
    def __init__(self, parent = None):
        """
        Constructs all the necessary attributes for the ViewDetailChart object.

        Parameters
        ----------
            None
        """
        wx.Frame.__init__(self, parent = parent, id=wx.ID_ANY, title="Data Analysis Software", pos=wx.DefaultPosition,
                          size= (900, 700), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.Maximize(True)
        self.screen_width, self.screen_height = self.GetSize()

        self.panel = wx.Panel(self)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        # start of logo section
        self.plot_sizer = wx.BoxSizer(wx.VERTICAL)

        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.logo = wx.StaticText(self, wx.ID_ANY, u"#Visualise", wx.DefaultPosition, wx.DefaultSize, 5)
        self.logo.SetForegroundColour(wx.Colour(94, 23, 235))
        # font for logo text
        font = wx.Font(16, family=wx.FONTFAMILY_SCRIPT, style=wx.FONTSTYLE_SLANT, weight=100,
                       underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        self.logo.SetFont(font)
        self.h_sizer.Add(self.logo, 0, wx.ALL, 20)

        self.h_sizer.AddStretchSpacer(1)
        self.plot_sizer.Add(self.h_sizer, 0, wx.ALL | wx.EXPAND, 5)

        self.line = wx.StaticLine(self, wx.ID_ANY, size=(self.screen_width, 1), style=wx.LI_HORIZONTAL)
        self.plot_sizer.Add(self.line)

        self.new_figure_score, axes = plt.subplots(nrows = 1, ncols = 1,constrained_layout = True)

        # group data based on cuisine and count based on violation code
        self.grouped_cuisine_all = pd.DataFrame(df.groupby("CUISINE DESCRIPTION")['VIOLATION CODE'].count())
        self.grouped_cuisine = self.grouped_cuisine_all.unstack()

        self.unique_cuisine = df['CUISINE DESCRIPTION'].unique()
        self.unique_cuisine.sort()

        # plot the data
        axes.bar(self.grouped_cuisine['VIOLATION CODE'].keys(), self.grouped_cuisine['VIOLATION CODE'].values)
        axes.set_title(u'Violation count per cuisine')
        axes.set_xlabel('Cuisine Description', labelpad=10, fontsize=10)
        axes.set_ylabel('Count of Violation', fontsize=10)
        axes.tick_params(axis='x', labelrotation=90)

        # canvas to add the plot
        self.new_canvas = FigureCanvasWxAgg(self, -1, self.new_figure_score)
        self.new_canvas.draw()
        self.plot_sizer.Add(self.new_canvas, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 10)
        self.SetSizer(self.plot_sizer)

        self.Layout()
        self.Show()