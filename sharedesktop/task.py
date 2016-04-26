import wx

ID_STAT = 1
ID_TOOL = 2

class CheckMenuItem(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(350, 250))

        # -------------------- taskbar ico code -------------------------------

        iconFile = "icon.ico"

        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)

        self.tbicon = wx.TaskBarIcon()
        self.tbicon.SetIcon(icon1, 'Application')

        self.Bind(wx.EVT_CLOSE, self.onCloseBox)
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.onTaskbarActivate)

        # -------------------- taskbar ico code -------------------------------

        menubar = wx.MenuBar()
        file = wx.Menu()
        view = wx.Menu()
        self.shst = view.Append(ID_STAT, 'Show statubar', 'Show Statusbar', kind=wx.ITEM_CHECK)
        self.shtl = view.Append(ID_TOOL, 'Show toolbar', 'Show Toolbar', kind=wx.ITEM_CHECK)
        view.Check(ID_STAT, True)
        view.Check(ID_TOOL, True)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, id=ID_STAT)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, id=ID_TOOL)

        menubar.Append(file, '&File')
        menubar.Append(view, '&View')
        self.SetMenuBar(menubar)


        self.statusbar = self.CreateStatusBar()
        self.Centre()
        self.Show(True)

    # ------------------------ events ------------------------

    # tried many things from examples but no luck!

    def onCloseBox(self, event):

        self.Show(False)


    def onTaskbarActivate(self, event):

        self.Show(True)

    # ------------------------ events ------------------------

    def ToggleStatusBar(self, event):
        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self, event):
        if self.shtl.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()

app = wx.App()
CheckMenuItem(None, -1, 'App')
app.MainLoop()
