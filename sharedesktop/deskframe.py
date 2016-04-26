#!/usr/bin/env python
# -*- coding: utf-8-*-
import wx
class Frame(wx.Frame):
    """Frame class that displays an image."""
    def __init__(self, parent=None, id=-1,
                 pos=wx.DefaultPosition, title='swfu screen broadcast!'):
        wx.Frame.__init__(self, parent, id, title,size=wx.DisplaySize())
        #self.panel = wx.Panel(self,-1)
        #self.flag=True


class App(wx.App):
    """Application class."""
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show()
        return True
def main():
    app = App()
    app.MainLoop()
if __name__ == '__main__':
    main()
    
