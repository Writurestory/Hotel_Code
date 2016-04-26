#!/usr/bin/env python
# -*- coding: utf-8-*-
#!/usr/bin/env python
# -*- coding: utf-8-*-
import wx,sys
from wx import xrc
import multiprocessing
import wxscr
class MyApp(wx.App):
    def OnInit(self):
        self.res=xrc.XmlResource('teacher_form.xrc')
        self.init_frame()
        return True
    def __del__(self,destroy):
        print "ssss destroy-----------"
    def init_frame(self):
        self.fm=self.res.LoadFrame(None,'wxmain')
        #self.icon = wx.Icon('logo.ico', wx.BITMAP_TYPE_ICO)
        #self.fm.SetIcon(self.icon)  
        #self.fm.tbicon=wx.TaskBarIcon()  
        #self.fm.tbicon.SetIcon(self.icon,"NetUM")

        self.fm.SetTitle(u"屏幕广播")
        self.tstart=xrc.XRCCTRL(self.fm,'WB_broadcast')
        self.texit=xrc.XRCCTRL(self.fm,'WB_exit')
        self.tstart.SetLabel(u'开始广播')
        self.texit.SetLabel(u'退出')
        self.fm.SetStatusText(u'西南林业大学计信学院',0)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.tstart_OnClick, self.tstart)
        self.Bind(wx.EVT_BUTTON, self.texit_OnClick, self.texit)
        self.fm.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.flag=True
        self.fm.Show()

    def tstart_OnClick(self,event):
        if self.tstart.GetValue():
            #self.capThread=wxscr.capScreen(self)
            #self.capThread.setDaemon(True)
            #self.capThread.start()
            self.readProc = multiprocessing.Process(target=wxscr.ScreenImgSend,args=())
            self.readProc.start()
            self.tstart.SetLabel(u'停止广播')
            print "ttttttt"
        else:
            self.flag=False
            self.readProc.stop()
            #self.capThread.close()
            #self.capThread.join()
            self.tstart.SetLabel(u'开始广播')
            print "xxxxxx"

    def texit_OnClick(self,event):
        self.flag=False
        #self.capThread.join()
        sys.exit()
    def OnCloseWindow(self, event):
        try:
            self.fm.Destroy()
            self.flag=False
            self.capThread.join()
            sys.exit()
        except Exception,e:
            print e
            pass


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app=MyApp()
    app.MainLoop()

    

