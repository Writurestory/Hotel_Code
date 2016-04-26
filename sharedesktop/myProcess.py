#!/usr/bin/env python
# -*- coding: utf-8-*-
import multiRecv
import multiprocessing,signal,threading
import wx
import time
import zlib,string
import deskframe


myLock=multiprocessing.Lock()
def getRemoteImg(_Queue):
    
        #signal.signal(signal.SIGTERM, self.handler);
    flag=True
    try:
        while flag:
            #lock.acquire()
            #self.g.size = multiRecv.Recv(self.g.imgList,self.g)
            multiRecv.Recv(_Queue)
            #print "xxxxxx"
            #lock.release() 
    except Exception,e:
        print e

class showRemoteImg(threading.Thread):
    
    def __init__(self,obj,_queue):
        self.g=obj
        self.g.flag=True
        self.queue=_queue
        threading.Thread.__init__(self)
        self.lock = threading.Condition()
        wximage= wx.Image("cursor.png",wx.BITMAP_TYPE_PNG) #定义一个图标
        #wximage.ConvertAlphaToMask(220)
        #wximage.ConvertAlphaToMask(220)
        self.curImg=wx.BitmapFromImage(wximage)
        #self.curImg=wximage.ConvertToBitmap()
        self.curImg.SetMask(wx.Mask(self.curImg,wx.WHITE)) 
        self.curSize=[self.curImg.GetWidth(),self.curImg.GetHeight()]
        #self.dc = wx.ClientDC(self.g)
        self.dc=None
	self.frame=obj
	self.org_data=''

    def run(self):
        #scDic={}
        try:
            #y=0
            #start=0
            while self.g.flag:
                time.sleep(0.01)
		self.org_data=self.queue.get()
		wx.CallAfter(self.g.handleData,self.org_data)
                
                #type=self.org_data[0:4]
                #if type=='img:':
                #    #show image on frame
                #    self.drawImgOnframe()
                #elif type=='ctl:':
                #    self.myCommand()

        except Exception,e:
            print e            
    def myCommand(self):
        try:
            strCmd=self.org_data[4:]
            if strCmd=='close':
		print "ssssssss"
		#print self.frame
                #self.frame.Close(True)
        except Exception,e:
	    print "xxxxxxx"
	    print e
            pass
	

