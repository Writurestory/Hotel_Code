#!/usr/bin/env python
# -*- coding: utf-8-*-
import threading
import time
import ros
import readcard
class getAusers(threading.Thread):
    
    def __init__(self,frame,obj):
        global condition
        self.fm=frame
        self.g=obj
        threading.Thread.__init__(self)
        self.lock =threading.Lock()  
        self.last = time.time()
    def run(self):
        
        try:
            while self.g.flag:
                Now = time.time()
                if Now-self.last<=20:
                    continue
                self.last=Now
                #time.sleep(1)
                self.lock.acquire()
                available_num=len(self.g.user_list)
                online_num=len(self.g.acu_list)
                _str=u"开通帐号 %d 个, 在线主机数 %d 个 (20秒刷新)" %(available_num,online_num)
                self.fm.SetStatusText(_str,1)
                self.g.acu_list = ros.listActiveUser()
                self.lock.release()
        except Exception,e:
            print e

            
            

class chkCard(threading.Thread):
    
    def __init__(self,frame,obj):
        self.fm=frame
        self.g=obj
        self.roomid=''
        threading.Thread.__init__(self)
        self.lock = threading.Condition()
        self.last = time.time()
    def run(self):
        
        try:
            while self.g.flag:
                Now = time.time()
                if Now-self.last<=2:
                    continue
                self.last=Now
                t  = readcard.getCardNum()
                if self.roomid != t:
                    if t=='':continue
                    self.roomid =t
                    
                    #启动
                    self.lock.acquire()
                    self.g.tuid.SetValue(t[-4:])
                    self.g.proc_user()
                    self.lock.release()               
        except Exception,e:
            print e