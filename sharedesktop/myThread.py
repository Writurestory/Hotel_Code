#!/usr/bin/env python
# -*- coding: utf-8-*-
import threading,multiRecv
import wx
import time
import zlib,string

class getRemoteImg(threading.Thread):
    
    def __init__(self,obj):
        self.g=obj
        self.g.flag=True
        threading.Thread.__init__(self)
        self.lock = threading.Condition()
    def run(self):
        
        try:
            while self.g.flag:
                self.lock.acquire()
                self.g.size = multiRecv.Recv(self.g.imgList,self.g)
                self.lock.release() 
        except Exception,e:
            print e
            
class showRemoteImg(threading.Thread):
    
    def __init__(self,obj):
        self.g=obj
        self.g.flag=True
        threading.Thread.__init__(self)
        self.lock = threading.Condition()
    def run(self):
        scDic={}
        try:
            y=0
            start=0
            while self.g.flag:
                time.sleep(0.1)
                for key,org_data in self.g.imgList.items():
                    position=org_data[4:20]
                    imgData=zlib.decompress(org_data[21:])
                    #print position
                    x=string.atoi(position[:4])
                    y=string.atoi(position[4:8])
                    w=string.atoi(position[8:12])
                    h=string.atoi(position[12:16])
                    #bmp=wx.BitmapFromBuffer(w,h,imgData)
                    #wx.StaticBitmap(parent=self.g,bitmap=bmp,size=[w,h],pos=[x,y])
                    #old_img=scDic.get(y,'')
                    #if old_img==imgData:
                    #    continue
                    #scDic[y]=imgData
                    bmp=wx.BitmapFromBuffer(w,h,imgData)
                    #wx.CallAfter(self.g.showImg,x,y,w,h)
                    wx.StaticBitmap(parent=self.g,bitmap=bmp,size=[w,h],pos=[x,y])
                
                time.sleep(0.01)
        except Exception,e:
            print e            
