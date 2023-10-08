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
filename = "DOHMH_New_York_City_Restaurant_Inspection_Results.csv"
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

        self.df = load_file(filename)

        # code for from date field
        self.from_text = wx.StaticText(self, wx.ID_ANY, u"From", wx.DefaultPosition, wx.DefaultSize, 10)
        self.from_text.Wrap(-1)
        filter_sizer.Add(self.from_text, 0, wx.TOP | wx.BOTTOM, 15)

        self.date_field1 = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)
        # set the date range
        date_range = get_date_range()
        valid_range = check_date_range(date_range)
        if valid_range:
            self.date_field1.SetRange(date_range[0], date_range[1])
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
        self.canvas.SetSize(size)
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
        self.figure_score, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(nrows=2, ncols=2, constrained_layout = True)

        # Plot 1
        # data grouped according to suburbs and counted based on violation code
        self.grouped_suburb_df = self.groupby_single_column(self.df, 'BORO', 'VIOLATION CODE')
        self.plot_pie(self.grouped_suburb_df, 'VIOLATION CODE')

        # Plot 2
        # data grouped based on cuisine and counted is generated on violation code
        self.grouped_cuisine = self.groupby_single_column(self.df, 'CUISINE DESCRIPTION', 'VIOLATION CODE')
        short_df = self.grouped_cuisine.head(10)
        self.plot_bar(short_df, 'VIOLATION CODE')

        # Plot 3
        # mapping of violation codes to animals
        violation_code_dict = {'04K': 'Rats', '04L': 'Mice', '04M': 'Roach', '04N': 'Flies', '04O': 'Other live animals'}
        filtered_df = self.add_new_col(self.df, violation_code_dict, 'VIOLATION CODE', 'ANIMALS').copy()
        filtered_df['INSPECTION DATE'] = pd.to_datetime(filtered_df['INSPECTION DATE'])

        # group the data by year
        self.grouped_animals = self.groupby_double_column(filtered_df, 'ANIMALS', 'INSPECTION DATE')
        self.ax3.cla()
        self.plot_line(self.grouped_animals, filtered_df)

        # Plot 4
        # data is grouped based on suburbs and counted is generated based animals
        self.grouped_suburbs = self.groupby_double_column(filtered_df, 'BORO', 'ANIMALS')
        self.plot_stakced_bar(self.grouped_suburbs, filtered_df)

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

        # the pandas series is converted to datetime
        self.filtered_dates_df = filter_data('INSPECTION DATE', self.df, self.min_date_limit, self.max_date_limit)
        self.filtered_suburb = self.groupby_single_column(self.filtered_dates_df, 'BORO', 'VIOLATION CODE')

        violation_code_dict = {'04K': 'Rats', '04L': 'Mice', '04M': 'Roach', '04N': 'Flies', '04O': 'Other live animals'}
        filtered_df_line = self.add_new_col(self.filtered_dates_df, violation_code_dict, 'VIOLATION CODE', 'ANIMALS').copy()
        self.filtered_animals_df = pd.DataFrame(filtered_df_line.groupby(['ANIMALS', pd.to_datetime(filtered_df_line['INSPECTION DATE']).dt.month])['INSPECTION DATE'].count())
        self.filtered_animals = self.filtered_animals_df.unstack()

        if len(self.filtered_suburb) > 0:
            self.ax1.cla()
            self.plot_pie(self.filtered_suburb, 'VIOLATION CODE')
            self.ax3.cla()
            self.plot_line(self.filtered_animals, filtered_df_line)

            self.canvas.draw()
            self.main_dash.Detach(self.canvas)
            self.main_dash.Add(self.canvas, 1, wx.LEFT | wx.RIGHT | wx.GROW, 20)
            self.SetSizer(self.main_dash)
        else:
            wx.MessageBox('No data available for the selected date range', 'Info', wx.OK | wx.ICON_INFORMATION)

    def groupby_single_column(self, data, grouping_col_name, counting_col_name):

        grouped_df = pd.DataFrame(data.groupby(grouping_col_name)[counting_col_name].count())
        grouped_df = grouped_df.unstack()

        return grouped_df

    def groupby_double_column(self, data, col_1, col_2):
        double_grouped_df = pd.DataFrame(data.groupby([col_1, col_2])[col_2].count())
        double_grouped_df = double_grouped_df.unstack()

        return double_grouped_df

    def plot_pie(self, grouped_data, index):
        pie_color_list = ["#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"]
        self.ax1.pie(grouped_data[index].values, labels = grouped_data[index].keys(), colors=pie_color_list, radius=2)
        self.ax1.set_title(u'Violation Distribution over Suburbs', loc='right')

        return self.ax1

    def plot_bar(self, data, col_name):

        self.ax2.bar(data[col_name].keys(), data[col_name].values)
        self.ax2.set_title(u'Violation count per cuisine')
        self.ax2.set_xlabel('Cuisine Description', labelpad=10, fontsize=9)
        self.ax2.set_ylabel('Count of violation', labelpad=10, fontsize=9)
        self.ax2.tick_params(axis='x', labelrotation=45)

        return self.ax2
    def plot_line(self, data, data1):
        color_list = ["#0060ff", "#0080ff", "#009fff", "#00bfff", "#00ffff"]
        for index in range(len(data)):
            self.ax3.plot(data.iloc[index]['INSPECTION DATE'].keys(), data.iloc[index]['INSPECTION DATE'].fillna(0).to_numpy(), color=color_list[index])
        self.ax3.legend(self.get_unique_col_values(data1, 'ANIMALS'), prop={"size": 6}, title='Animals')
        self.ax3.set_title(u'Distribution of violation related to animals over time period')
        self.ax3.set_xlabel('Year')
        self.ax3.set_ylabel('Count of violation')

        return self.ax3
    def plot_stakced_bar(self, data, data1):
        bar_color_list = ["#363445", "#48446e", "#5e569b", "#776bcd", "#9080ff"]
        data.plot.bar(stacked=True, ax=self.ax4, color=bar_color_list, title='Violation related to animals over suburbs')
        self.ax4.legend(self.get_unique_col_values(data1, 'ANIMALS'), prop={"size": 6}, title='Animals')
        self.ax4.set_xticklabels(labels=self.grouped_suburbs.reset_index()['BORO'], rotation=0)

        return self.ax4

    def get_unique_col_values(self, data, col_name):
        unique_values = data[col_name].unique()

        return unique_values

    def add_new_col(self, data, mapping_dict, col_name, new_col_name):
        mapped_df = data[data[col_name].isin(['04K', '04L', '04M', '04N', '04O'])].copy()
        mapped_df[new_col_name] = mapped_df[col_name].map(mapping_dict)

        return mapped_df

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