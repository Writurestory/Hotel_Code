#!/usr/bin/env python
# -*- coding: utf-8-*-
import wx
import  sys
import random
from wx import xrc
from myTable import myTable
import  wx.grid             as  gridlib
import ros,myPrint
import thread,time
import myconf
import readcard
import winsound

class MyApp(wx.App):
    #mutex = threading.Lock()  
    def OnInit(self):
        self.acu_list=[]
        self.PWDSTR='qwertyuiopasdfghjklzxcvbnm'
        self.res=xrc.XmlResource('hotelForm.xrc')
        self.cardPrefix=myconf.getCardPrefix()
        self.ESSID=myconf.getESSID()
        self.init_frame()
        return True
    def __del__(self,destroy):
        print "ssss destroy-----------"
    def init_frame(self):
        self.fm=self.res.LoadFrame(None,'frame1')
        self.icon = wx.Icon('logo.ico', wx.BITMAP_TYPE_ICO)
        self.fm.SetIcon(self.icon)  
        self.fm.tbicon=wx.TaskBarIcon()  
        self.fm.tbicon.SetIcon(self.icon,"NetUM")

        self.tbar=xrc.XRCCTRL(self.fm,'toolbar')
        self.tuid=xrc.XRCCTRL(self.fm,'txtNum')
        self.grid1=xrc.XRCCTRL(self.fm,'grid_1')
        self.leftpannel=xrc.XRCCTRL(self.fm,'leftPannel')
        self.userinfo=xrc.XRCCTRL(self.fm,'userInfo')
        self.grid1.EnableEditing(False)
        self.grid1.SetSelectionBackground('red')
        self.statusbar=xrc.XRCCTRL(self.fm,'stausbar')
        self.fm.SetStatusText(u'网络用户管理系统',0)
        self.fm.SetStatusText(u'昆明炫点科技&西南林业大学 联合开发',2)
        self.btnToggle=xrc.XRCCTRL(self.fm,'btnFunc')
        self.Bind(wx.EVT_BUTTON, self.btnToggle_OnClick, self.btnToggle)
        self.tuid.Bind(wx.EVT_TEXT_ENTER,self.btnToggle_OnClick)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK,self.OnSelectUser)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK,self.OnSelectUser)
        self.fm.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.showPicture()
        self.showUserInfo()
        #print self.user_list
        self.fm.Show()
        self.myThread_start()
        self.roomid=''
        self.chkCardThread_start()
    def OnCloseWindow(self, event):
        try:
            self.fm.Destroy()
            sys.exit()
        except Exception,e:
            print e
            pass

    def myThread_start(self):
        try:
            available_num=len(self.user_list)
            online_num=len(self.acu_list)
            _str=u"开通帐号 %d 个, 在线主机数 %d 个" %(available_num,online_num)
            #print _str
            self.fm.SetStatusText(_str,1)
            thread.daemon=True
            thread.start_new_thread(self.listAUser,())
        except Exception,e:
            pass
    def chkCardThread_start(self):
        try:
            thread.daemon=True
            thread.start_new_thread(self.chkCardThread,())
        except Exception,e:
            pass
    def chkCardThread(self):
        t = readcard.getCardNum()
        if self.roomid != t:
            self.roomid =t
            #启动
            self.tuid.SetValue(self.roomid[-4:])
            self.proc_user()
        time.sleep(2)
        self.chkCardThread_start()
            
    def listAUser(self):
        #while 1:
        time.sleep(30)
            #print "---------"
        self.acu_list = ros.listActiveUser()
        self.myThread_start()
        
    def showPicture(self):
        try:
            jpg = wx.Image('left.jpg', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
            wx.StaticBitmap(self.leftpannel, -1, jpg, (0,0), (jpg.GetWidth(), jpg.GetHeight()))
        except Exception,e:
            print e
          
    def checkUser(self,_user):
        _user="".join(_user.split()); 
        ret=''
        try:
            t=int(_user)
            return _user
        except:
            return ''
        
        
        try:
            if len(_user)==10:
                #检查卡号的前几位
                l=len(self.cardPrefix)
                if _user[0:l]!=self.cardPrefix: return ''
                t=int(_user[-4:])
                #ret= "%04x" %t
                return str(t)
            elif len(_user)==4:
                int(_user,16)
                return _user
            else:
                return ''
        except:
            return ''

    def OnSelectUser(self,evt):
        self.current_user=self.user_list[evt.GetRow()][1]
        #1.查找该用户的当前状态
        #self.selectedRow=evt.GetRow()
        self.tuid.SetValue(self.current_user)
        #显示用户的当前网络状态
        #print "----------------------------------------"
        data = ros.activeUserInfo(self.current_user,self.acu_list)
        str=u'帐号: %s\n' %self.current_user
        str += u'登陆次数: %d 次 \n\n' % len(data)
        for d in data:
            for t in d:
                if t=='!re': continue
                ta=t.split('=')
                #print ta
                str += "%s: %s\n" %(myconf._(ta[1]),ta[2])
            str += '\n\n'

        self.userinfo.SetLabel(str)
        self.grid1.SelectRow(evt.GetRow(),0)
        #evt.Skip()

    def proc_user(self):
        #print "enter-----------"
        #2.修改数据库中的用户状态
        _user=str(self.tuid.GetValue())
        if _user == '': return
        u=self.checkUser(_user)
        
        if u == '':
            dlg = wx.MessageDialog(None, u'你输入的帐号不正确', u'帐号错误', wx.OK |wx.ICON_ERROR|wx.STAY_ON_TOP)  
            result = dlg.ShowModal()
            dlg.Destroy()
            self.tuid.SetValue('')
            return

        self.current_user=u

        #print "ssss:"+self.current_user
        newPwd=self.getNewPwd()
        #判断文本框中的用户是否已经存在


        uPosition = -1
        for i in range(0,len(self.user_list)):
            if self.user_list[i][1]==self.current_user: 
                uPosition = i
                break
        #print "uPos %d" %uPosition

        if uPosition != -1:
            #存在,则删除用户,禁止使用
            userid=self.user_list[uPosition][0]
            user=self.user_list[uPosition][1]
            ros.delUser(userid,user)
            winsound.Beep(4000,300)
        else:
            #若不存在,添加用户并启用
            ros.addNewUser(self.current_user,newPwd)
            winsound.Beep(3000,300)
            myPrint.send_to_printer(self.ESSID,self.current_user,newPwd)

        
        self.showUserInfo()
        self.grid1.ForceRefresh()
        self.tuid.SetValue('')

    def btnToggle_OnClick(self,evt):
        self.proc_user()
        evt.Skip()


        
    def showUserInfo(self):
        try:
            self.user_list=ros.getUserList()
            self.user_blocked_list=[]
            mytable=myTable(self.user_list)
            self.grid1.SetTable(mytable,True)
        except Exception,e:
            dlg = wx.MessageDialog(None, u'错误号码:'+str(e[0])+'\n\n'+e[1], u'系统', wx.OK |wx.ICON_ERROR|wx.STAY_ON_TOP)  
            result = dlg.ShowModal()
            dlg.Destroy()
            sys.exit()


    def getNewPwd(self):
        lst=list(self.PWDSTR)
        slice = random.sample(lst, 6)
        return ''.join(slice)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app=MyApp()
    app.MainLoop()
