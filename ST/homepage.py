"""
This file contains classes and methods necessary for the homepage
This file contains :
    HomePage - main class for home page
    DataTable - class to create a grid
"""
import wx
import wx.adv
import pandas as pd
import wx.grid
import datetime
from common import *

filename = "DOHMH_New_York_City_Restaurant_Inspection_Results.csv"
# data file used for analysis
# df = pd.read_csv(r"DOHMH_New_York_City_Restaurant_Inspection_Results.csv")


class HomePage(wx.Panel):
    """
    A class for creating the home page.

    This class contains all the methods and events for the home page

    Attributes
    ----------
        None

    Methods
    -------
        OnResetFilter
            This method will reset all the filters and load the initial data in the grid in home page

        OnFromDateSelected
            This method will enable the to date field and set the minimum date range

        OnDateSelected
            This method will filter the data based on the from and to date and reload the datatable

        OnColSelect
            This method will perform operations related to the select field

        OnSearchKeyword
            This method will search for keyword specified in the column in the select field

        OnExportToCSV
            This method will export data that is currently displayed in the data grid to csv format

        SetDataTable
            This method is used to set the datatable after applying filters
    """
    def __init__(self, parent):
        """
        Constructs all the necessary attributes for the HomePage object.

        Parameters
        ----------
            None
        """
        wx.Panel.__init__(self, parent = parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Code for the filter section
        filter_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # code to load the data file
        self.df = load_file(filename)

        # code for from date
        self.from_text = wx.StaticText(self, wx.ID_ANY, u"From", wx.DefaultPosition, wx.DefaultSize, 10)
        self.from_text.Wrap(-1)
        filter_sizer.Add(self.from_text, 0, wx.TOP|wx.BOTTOM, 15)

        self.date_field1 = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)
        # self.date_field1.Bind(wx.adv.EVT_DATE_CHANGED, self.OnFromDateSelected)
        date_range = get_date_range()
        valid_range = check_date_range(date_range)
        if valid_range:
            self.date_field1.SetRange(date_range[0], date_range[1])
        self.date_field1.Bind(wx.adv.EVT_DATE_CHANGED, self.OnFromDateSelected)
        filter_sizer.Add(self.date_field1, 0, wx.ALL, 10)

        # code for to date
        self.to_text = wx.StaticText(self, wx.ID_ANY, u"To", wx.DefaultPosition, wx.DefaultSize, 10)
        self.to_text.Wrap(-1)
        filter_sizer.Add(self.to_text, 0, wx.TOP|wx.BOTTOM, 15)

        self.date_field2 = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)
        filter_sizer.Add(self.date_field2, 0, wx.ALL, 10)
        self.date_field2.Disable()

        # initialise view button
        btn = wx.Button(self, label='View', size = (110, 35))
        btn.SetForegroundColour(wx.Colour(255, 255, 255))
        btn.SetBackgroundColour(wx.Colour(4, 139, 74))
        filter_sizer.Add(btn, 0, wx.ALL, 5)
        btn.Bind(wx.EVT_BUTTON, self.OnDateSelected)

        # initialise choice / select field
        self.excluded_col_list = ['CAMIS', 'BUILDING', 'ZIPCODE', 'PHONE', 'INSPECTION DATE', 'SCORE', 'GRADE', 'GRADE DATE', 'RECORD DATE']
        # col_list = set(self.df.columns)
        # exclusion_set = set(excluded_col_list)
        # self.choices = sorted(list(col_list - exclusion_set))
        self.choices = self.get_col_choices(self.excluded_col_list, self.df.columns)
        self.col_choice = wx.ComboBox(self, size = (150, 35), choices=self.choices, value="Select a column")
        self.Bind(wx.EVT_TEXT, self.OnColSelect)
        self.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.OnColSelect)
        filter_sizer.AddStretchSpacer(1)
        filter_sizer.Add(self.col_choice, 1, wx.ALL, 5)

        # initialise the text field for keyword search
        self.textCtrl = wx.TextCtrl(self, wx.TEXT_ALIGNMENT_CENTER, size = (250, 30))
        self.textCtrl.SetHint('Enter a keyword..')
        self.textCtrl.Disable()
        filter_sizer.Add(self.textCtrl, 0, wx.ALL|wx.ALIGN_LEFT, 5)

        # initialise the search button for keyword search
        self.search_btn = wx.Button(self, label='Search', size=(110, 35))
        self.search_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.search_btn.SetBackgroundColour(wx.Colour(4, 139, 74))
        self.search_btn.Bind(wx.EVT_BUTTON, self.OnSearchKeyword)
        filter_sizer.Add(self.search_btn, 0, wx.ALL, 5)

        # initialise reset button to undo all filters
        self.reset_btn = wx.Button(self, label='Reset', size=(110, 35))
        self.reset_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.reset_btn.SetBackgroundColour(wx.Colour(170, 170, 170))
        self.reset_btn.Bind(wx.EVT_BUTTON, self.OnResetFilter)
        filter_sizer.Add(self.reset_btn, 0, wx.ALL, 5)

        # initialise export button
        self.export_btn = wx.Button(self, label='Export', size = (110, 35))
        self.export_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.export_btn.SetBackgroundColour(wx.Colour(4, 139, 74))
        self.export_btn.Bind(wx.EVT_BUTTON, self.OnExportToCSV)
        filter_sizer.Add(self.export_btn, 0, wx.ALL , 5)

        self.sizer.Add(filter_sizer, 0, wx.ALL | wx.EXPAND, 10)
        # end of filter section

        # initialise data grid
        self.data_grid = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        self.df_1 = self.df.copy()
        self.columns = self.df.columns
        self.table = DataTable(self.df.fillna(''))
        self.export_data = self.df.copy()
        self.data_grid.SetTable(self.table, takeOwnership=False)
        self.data_grid.EnableEditing(False)
        self.sizer.Add(self.data_grid, 0, wx.ALL | wx.EXPAND | wx.GROW, 15)
        self.SetSizer(self.sizer, wx.EXPAND | wx.GROW)

    def OnResetFilter(self, e):
        """
        This method will reset the date and keyword search field in the filter section.
        The initial data will be loaded in the data grid.

        Parameters
        ----------
            event
                The event that triggers the function call

        Returns
        -------
            None
        """
        self.date_field1.SetRange(datetime.datetime(1900, 1, 1), datetime.datetime(2017, 12, 31))
        self.date_field2.Disable()
        self.col_choice.SetValue('')
        self.textCtrl.Disable()
        self.export_data = self.df.copy()
        self.SetDataTable(self.df)

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
        valid_range = check_date_range([self.min_date_limit, self.max_date_limit])

        if valid_range:
            # the pandas series is converted to datetime
            self.datetime_converted_1 = pd.to_datetime(self.df['INSPECTION DATE'], infer_datetime_format=True)
            self.df_1 = self.df[self.datetime_converted_1 >= datetime.datetime(self.min_date_limit.year, self.min_date_limit.month + 1, self.min_date_limit.day)]

            self.datetime_converted_2 = pd.to_datetime(self.df_1['INSPECTION DATE'], infer_datetime_format=True)
            self.df_1 = self.df_1[self.datetime_converted_2 <= datetime.datetime(self.max_date_limit.year, self.max_date_limit.month + 1, self.max_date_limit.day)]

            if len(self.df_1) > 0:
                self.SetDataTable(self.df_1)
            else:
                wx.MessageBox('No data available for the selected date range', 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Please choose a valid date range', 'Info', wx.OK | wx.ICON_INFORMATION)

    def get_col_choices(self, excluded_list, all_column_names):

        col_list = set(all_column_names)
        exclusion_set = set(excluded_list)
        col_choices = sorted(list(col_list - exclusion_set))

        return col_choices

    def check_column_name(self, column_name, valid_col_choices):

        return column_name in valid_col_choices

    def OnColSelect(self, event):
        """
        This method enable the keyword search text field when a valid choice is made.
        If the value is invalid or if it is empty, a message will be displayed.

        Parameters
        ----------
            event
                The event that triggers the function call

        Returns
        -------
            None
        """
        self.chosen_col = self.col_choice.GetValue().upper()

        valid_column = self.check_column_name(self.chosen_col, self.choices)
        if valid_column:
            self.textCtrl.Enable()
        elif len(str(self.chosen_col)) == 0:
            pass
        else:
            wx.MessageBox('Please choose a column from the dropdown', 'Info', wx.OK | wx.ICON_INFORMATION)

    def OnSearchKeyword(self, e):
        """
        This method will filter the data based on the keyword entered in the text field.
        If the keyword is not in any of the rows of the specified column,
        a message will be displayed.

        Parameters
        ----------
            event
                The event that triggers the function call

        Returns
        -------
            None
        """
        self.keyword = self.textCtrl.GetValue()
        if len(self.keyword) > 0:
            if len(self.df_1) > 0:
                temp_df = self.df_1.fillna('').copy()
            else:
                temp_df = self.df.fillna('').copy()
            temp_df = temp_df[temp_df[str(self.chosen_col)].str.contains(self.keyword, case = False)]
            if len(temp_df) > 0:
                self.SetDataTable(temp_df)
            else:
                wx.MessageBox('No data match for ' + self.keyword, 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Please enter a keyword to search', 'Info', wx.OK | wx.ICON_INFORMATION)

    def OnExportToCSV(self, e):
        """
        This method will export the current data displayed to csv format.

        Parameters
        ----------
            event
                The event that triggers the function call

        Returns
        -------
            None
        """
        self.export_data.to_csv("output.csv", index = False)
        wx.MessageBox('Data exported successfully!!', 'Info', wx.OK | wx.ICON_INFORMATION)

    def SetDataTable(self, data):
        """
        This method will reinitialise the data grid after applying filters.

        Parameters
        ----------
            event
                The event that triggers the function call

        Returns
        -------
            None
        """
        temp_table = DataTable(data.fillna(''))
        self.export_data = data.copy()
        self.data_grid.ClearGrid()
        self.data_grid.SetTable(temp_table, True)
        self.data_grid.EnableEditing(False)
        self.sizer.Detach(self.data_grid)
        self.sizer.Add(self.data_grid)
        self.SetSizer(self.sizer)

EVEN_ROW_COLOUR = '#f3f3f3'
GRID_LINE_COLOUR = '#ccc'

class DataTable(wx.grid.GridTableBase):
    """
    A class for creating the data grid.
    This class contains all the methods and events to initialise the data grid

    Reference: https://docs.wxpython.org/wx.grid.GridTableBase.html
    """
    def __init__(self, data=None):
        wx.grid.GridTableBase.__init__(self)
        self.headerRows = 1
        self.data = data

    def GetNumberRows(self):
        return len(self.data.index)

    def GetNumberCols(self):
        # return len(self.data.columns)
        return len(self.data.columns)

    def GetValue(self, row, col):
        # format date for the 'INSPECTION DATE' column
        if col in [8, 15, 16] and len(str(self.data.iloc[row, col])) > 0 and self.data.iloc[row, col] != 'nan':
            self.datetime_object = datetime.datetime.strptime(str(self.data.iloc[row, col]), '%m/%d/%Y').date()

            return self.datetime_object
        else:
            return self.data.iloc[row, col]

    # For better visualisation
    def GetColLabelValue(self, col):
        return self.data.columns[col]

    def GetAttr(self, row, col, prop):
        attr = wx.grid.GridCellAttr()
        if row % 2 == 1:
            attr.SetBackgroundColour(EVEN_ROW_COLOUR)

        return attr