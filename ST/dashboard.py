"""
This file contains classes and methods for the dashboard page.
This file contains :
    Dashboard - main class for dashboard page

Reference: https://wiki.wxpython.org/How%20to%20use%20Matplotlib%20-%20Part%201%20%28Phoenix%29
"""
import wx
import wx.adv
import datetime
import pandas as pd

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import matplotlib.pyplot as plt
from viewdetail import ViewDetailChart
from common import *
# data file used for analysis
# df = pd.read_csv(r"DOHMH_New_York_City_Restaurant_Inspection_Results.csv")

class Dashboard(wx.Panel):
    """
    A class for Dashboard page.

    This class contains all the basic methods for the dashboard page

    Attributes
    ----------
        None

    Methods
    -------
        plotdata
            This method will plot all the charts in the dashboard page

        OnFromDateSelected
            This method will enable the to date field and set the minimum date range

        OnDateSelected
            This method will filter the data based on the from and to date and reload the datatable

        OnViewAll
            This method will call ViewDetailChart class to display a detailed plot in a new frame
    """
    def __init__(self, parent, size):
        """
        Constructs all the necessary attributes for the HomePage object.

        Parameters
        ----------
           None
        """
        wx.Panel.__init__(self, parent = parent)
        self.main_dash = wx.BoxSizer(wx.VERTICAL)

        # code for filter section
        filter_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.df = load_file()

        # code for from date field
        self.from_text = wx.StaticText(self, wx.ID_ANY, u"From", wx.DefaultPosition, wx.DefaultSize, 10)
        self.from_text.Wrap(-1)
        filter_sizer.Add(self.from_text, 0, wx.TOP | wx.BOTTOM, 15)

        # self.date_field1 = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)
        # self.date_field1.SetRange(datetime.datetime(1900, 1, 1), datetime.datetime(2017, 12, 31))
        self.date_field1 = set_from_date(self)
        self.date_field1.Bind(wx.adv.EVT_DATE_CHANGED, self.OnFromDateSelected)
        filter_sizer.Add(self.date_field1, 0, wx.ALL, 10)

        # code for to date field
        self.to_text = wx.StaticText(self, wx.ID_ANY, u"To", wx.DefaultPosition, wx.DefaultSize, 10)
        self.to_text.Wrap(-1)
        filter_sizer.Add(self.to_text, 0, wx.TOP | wx.BOTTOM, 15)

        self.date_field2 = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)
        filter_sizer.Add(self.date_field2, 0, wx.ALL, 10)
        self.date_field2.Disable()

        # code for view button for date field
        btn = wx.Button(self, label='View', size=(110, 35))
        btn.SetForegroundColour(wx.Colour(255, 255, 255))
        btn.SetBackgroundColour(wx.Colour(4, 139, 74))
        filter_sizer.Add(btn, 0, wx.ALL, 5)
        btn.Bind(wx.EVT_BUTTON, self.OnDateSelected)

        # code for the button that links to ViewDetailChart class for detailed plot display
        self.viewall_btn = wx.Button(self, label='View all', size=(110, 35))
        self.viewall_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.viewall_btn.SetBackgroundColour(wx.Colour(4, 139, 74))
        self.viewall_btn.SetToolTip("View violations across all cuisines")
        self.viewall_btn.Bind(wx.EVT_BUTTON, self.OnViewAll)
        filter_sizer.AddStretchSpacer(1)
        filter_sizer.Add(self.viewall_btn, 0, wx.RIGHT | wx.TOP, 5)

        self.main_dash.Add(filter_sizer, 0, wx.ALL | wx.EXPAND, 10)

        self.figure_score = self.plot_data()
        # canvas for plotting the charts
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure_score)
        self.canvas.SetSize(parent.GetSize())
        self.canvas.draw()

        self.main_dash.Add(self.canvas, 1, wx.LEFT | wx.RIGHT | wx.GROW , 20)
        self.SetSizer(self.main_dash)
        self.Layout()

    def plot_data(self):
        """
        This method will plot all the data in subplot in a single figure

        Parameters
        ----------
            None

        Returns
        -------
            figure_score
                This will a figure containing all the plots
        """
        self.figure_score, ((self.ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, constrained_layout = True)

        # Plot 1
        # data grouped according to suburbs and counted based on violation code
        self.grouped_suburb_df = pd.DataFrame(self.df.groupby("BORO")['VIOLATION CODE'].count())
        self.grouped_suburb = self.grouped_suburb_df.unstack()

        self.unique_suburb = df['BORO'].unique()
        self.unique_suburb.sort()
        pie_color_list = ["#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"]
        self.ax1.pie(self.grouped_suburb['VIOLATION CODE'].values, labels = self.unique_suburb, colors = pie_color_list, radius = 2)
        self.ax1.set_title(u'Violation Distribution over Suburbs', loc = 'right')

        # Plot 2
        # data grouped based on cuisine and counted is generated on violation code
        self.grouped_cuisine_df = pd.DataFrame(self.df.groupby("CUISINE DESCRIPTION")['VIOLATION CODE'].count())
        self.grouped_cuisine = self.grouped_cuisine_df.unstack()
        short_df = self.grouped_cuisine.head(10)

        ax2.bar(short_df['VIOLATION CODE'].keys(), short_df['VIOLATION CODE'].values)
        ax2.set_title(u'Violation count per cuisine')
        ax2.set_xlabel('Cuisine Description', labelpad=10, fontsize=9)
        ax2.set_ylabel('Count of violation', labelpad=10, fontsize=9)
        ax2.tick_params(axis='x', labelrotation=45)

        # Plot 3
        # mapping of violation codes to animals
        filtered_df = self.df[self.df['VIOLATION CODE'].isin(['04K', '04L', '04M', '04N', '04O'])].copy()
        violation_code_dict = {'04K': 'Rats', '04L': 'Mice', '04M': 'Roach', '04N': 'Flies', '04O': 'Other live animals'}
        filtered_df['ANIMALS'] = filtered_df['VIOLATION CODE'].map(violation_code_dict)

        filtered_df['INSPECTION DATE'] = pd.to_datetime(filtered_df['INSPECTION DATE'])

        # group the data by year
        self.grouped_animals_df = pd.DataFrame(filtered_df.groupby(['ANIMALS', filtered_df['INSPECTION DATE'].dt.year])['INSPECTION DATE'].count())
        self.grouped_animals = self.grouped_animals_df.unstack()
        self.unique_animals = filtered_df['ANIMALS'].unique()

        self.grouped_date_df = pd.DataFrame(filtered_df.groupby([filtered_df['INSPECTION DATE'].dt.year, 'ANIMALS'])['ANIMALS'].count())
        self.grouped_date = self.grouped_date_df.unstack()
        self.unique_dates = filtered_df['INSPECTION DATE'].dt.year.unique()
        self.unique_dates.sort()

        color_list = [ "#0060ff", "#0080ff", "#009fff", "#00bfff", "#00ffff"]
        for index in range(len(self.grouped_animals)):
            ax3.plot(self.unique_dates, self.grouped_animals.iloc[index].fillna(0).to_numpy(),'o-.', color = color_list[index])
        ax3.legend(self.unique_animals, prop = { "size": 6 }, title = 'Animals')
        ax3.set_title(u'Distribution of violation related to animals over time period')
        ax3.set_xlabel('Year')
        ax3.set_ylabel('Count of violation')

        # Plot 4
        # data is grouped based on suburbs and counted is generated based animals
        self.grouped_suburbs_df = pd.DataFrame(filtered_df.groupby(['BORO', 'ANIMALS'])['ANIMALS'].count())
        self.grouped_suburbs = self.grouped_suburbs_df.unstack()

        bar_color_list = ["#363445", "#48446e", "#5e569b", "#776bcd", "#9080ff"]
        self.grouped_suburbs.plot.bar(stacked=True, ax = ax4, color = bar_color_list, title = 'Violation related to animals over suburbs')
        ax4.legend(self.unique_animals, prop = { "size": 6 }, title = 'Animals')
        ax4.set_xticklabels(labels = self.grouped_suburbs.reset_index()['BORO'], rotation = 0)

        return self.figure_score

    def OnFromDateSelected(self, e):
        """
        This method will set the minimum date for the 'to' date field.

        Parameters
        ----------
            event
                The event that triggers the function call

        Returns
        -------
            None
        """
        self.min_date_limit = self.date_field1.GetValue()
        self.date_field2.SetRange(datetime.datetime(self.min_date_limit.year, self.min_date_limit.month + 1, self.min_date_limit.day), datetime.datetime(2017, 12, 31))
        self.date_field2.Enable()

    def OnDateSelected(self, e):
        """
        This method will filter the data based on the 'from' and 'to' dates.
        A new plot is generated in the place of #Plot 1
        For an empty dataset, an information will be displayed.

        Parameters
        ----------
            event
                The event that triggers the function call

        Returns
        -------
            None
        """
        self.min_date_limit = self.date_field1.GetValue()
        self.max_date_limit = self.date_field2.GetValue()

        # the pandas serie is converted to datetime
        self.datetime_converted_1 = pd.to_datetime(self.df['INSPECTION DATE'], infer_datetime_format=True)
        self.filtered_df_pie = df[self.datetime_converted_1 >= datetime.datetime(self.min_date_limit.year, self.min_date_limit.month + 1, self.min_date_limit.day)]

        self.datetime_converted_2 = pd.to_datetime(self.filtered_df_pie['INSPECTION DATE'], infer_datetime_format=True)
        self.filtered_df_pie = self.filtered_df_pie[self.datetime_converted_2 <= datetime.datetime(self.max_date_limit.year, self.max_date_limit.month + 1, self.max_date_limit.day)]

        self.filtered_suburb_df = pd.DataFrame(self.filtered_df_pie.groupby("BORO")['VIOLATION CODE'].count())
        self.filtered_suburb = self.filtered_suburb_df.unstack()

        if len(self.filtered_suburb) > 0:
            pie_color_list = ["#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"]
            self.ax1.pie(self.filtered_suburb['VIOLATION CODE'].values, colors=pie_color_list, radius=2)
            self.ax1.set_title(u'Violation Distribution over Suburbs', loc='right')

            self.canvas.draw()
            self.main_dash.Detach(self.canvas)
            self.main_dash.Add(self.canvas, 1, wx.LEFT | wx.RIGHT | wx.GROW, 20)
            self.SetSizer(self.main_dash)
        else:
            wx.MessageBox('No data available for the selected date range', 'Info', wx.OK | wx.ICON_INFORMATION)

    def OnViewAll(self, e):
        """
        This method will call the class to display the detailed chart in a new frame

        Parameters
        ----------
            None

        Returns
        -------
            None
        """
        ViewDetailChart()