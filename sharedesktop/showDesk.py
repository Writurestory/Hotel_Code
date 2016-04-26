#!/usr/bin/env python
# -*- coding: utf-8-*-
import wx
import Image,zlib,base64,string
import multiRecv
import threading,myProcess,myThread
import multiprocessing

class Frame(wx.Frame):
    """Frame class that displays an image."""
    def __init__(self, parent=None, id=-1,
                 pos=wx.DefaultPosition, title='Hello, wxPython!'):
        wx.Frame.__init__(self, parent, id, title,size=wx.DisplaySize())
        #self.panel = wx.Panel(self,-1)
        self.flag=True
        #self.Bind(wx.EVT_PAINT, self.OnPaint)


	wximage= wx.Image("cursor.png",wx.BITMAP_TYPE_PNG) #定义一个图标
        self.curImg=wx.BitmapFromImage(wximage)
        self.curImg.SetMask(wx.Mask(self.curImg,wx.WHITE)) 
        self.curSize=[self.curImg.GetWidth(),self.curImg.GetHeight()]
	self.dc = wx.ClientDC(self)



        self.myQueue=multiprocessing.Queue(5)
        self.readProc = multiprocessing.Process(target=myProcess.getRemoteImg,args=(self.myQueue,))
        self.readProc.start()
        self.showImgThread=myProcess.showRemoteImg(self,self.myQueue)
        self.showImgThread.setDaemon(True)
        self.showImgThread.start()

    def handleData(self,data):
        type=data[0:4]
	#print type
        if type=='img:':#show image on frame
	    self.drawImgOnframe(data)
        elif type=='ctl:':
	    cmd_str=data[4:]
            self.myCommand(cmd_str)

    def myCommand(self,cmd_str):
        try:
            if cmd_str=='close':
		#print self.frame
                self.ShowFullScreen(False)
		self.Show(False)
        except Exception,e:
	    print "close frame failure"

    def drawImgOnframe(self, org_data):
	try:
	    #print "show img"
            position=org_data[4:28]
            imgData=zlib.decompress(org_data[29:])
            x=string.atoi(position[:4])
            y=string.atoi(position[4:8])
            w=string.atoi(position[8:12])
            h=string.atoi(position[12:16])
            cur_x=string.atoi(position[16:20])
            cur_y=string.atoi(position[20:24])
            bmp=wx.BitmapFromBuffer(w,h,imgData)
	    if self.IsShown():
                dc = wx.ClientDC(self)
       		self.curImg.SetMask(wx.Mask(self.curImg,wx.BLACK)) 
	        dc.DrawBitmap(bmp, x,y, True)
        	dc.DrawBitmap(self.curImg, cur_x-14,cur_y-7, True)
	    else:
	   	self.ShowFullScreen(True)              
	except Exception,e:
	   print "show img error"
	   print e        

class App(wx.App):
    """Application class."""
    def OnInit(self):
        self.flag=True
        self.frame = Frame()
	#	self.frame.ShowFullScreen(True)
        #self.Bind(wx.EVT_PAINT, self.OnPaint)
        #self.myQueue=multiprocessing.Queue(5)
        #self.readProc = multiprocessing.Process(target=myProcess.getRemoteImg,args=(self.myQueue,))
        #self.readProc.start()
        #self.showImgThread=myProcess.showRemoteImg(self,self.myQueue)
        #self.showImgThread.setDaemon(True)
        #self.showImgThread.start()


        #self.frame.Show()
        return True
def main():
    app = App()
    app.MaxinLoop()
if __name__ == '__main__':
    main()
    
