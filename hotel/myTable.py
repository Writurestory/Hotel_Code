# -*- coding: utf-8-*-
import  wx
import  wx.grid             as  gridlib
import  wx.lib.gridmovers   as  gridmovers

class myTable(gridlib.PyGridTableBase):
    def __init__(self,_ulist):
        gridlib.PyGridTableBase.__init__(self)
        self.colLabels = [u'编号',u'上网帐号',u'密码',u'状态']
        #self.getDatafromMysql()
        #self.data=_data
        self.user_list=_ulist
        #self.user_blocked_list=_bulist
    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface

    #def getDatafromMysql(self):
    #    m=radMysql()
    #    self.user_list=m.getRadUsers()
    #    self.user_blocked_list=m.getRadBlockedUsers()
        
    def GetNumberRows(self):

        return len(self.user_list)

    def GetNumberCols(self):
        return len(self.colLabels)
        

    def IsEmptyCell(self, row, col):
        #id = self.identifiers[col]
        return not self.user_list[row][col]

    def GetValue(self, row, col):
        #id = self.identifiers[col]
        uid = self.user_list[row][0]
        return self.user_list[row][col]
    def SetValue(self, row, col, value):
        #id = self.identifiers[col]
        self.user_list[row][col] = value

    def GetColLabelValue(self, col):
        return self.colLabels[col]

