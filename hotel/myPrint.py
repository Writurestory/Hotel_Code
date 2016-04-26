# -*- coding: utf-8-*-
#--------------------- 
import sys,math
import win32ui 
import win32print 
import win32con
def send_to_printer(essid,username,pwd): 
    str=[u'酒店网络账号', u'用户名：****', u'密码：******',  u'网络账号退房时失效',u'.',u'-------使用说明-------',u'.']
    str[0]=u'无线： '+ essid
    str[1]=u'用户名: '+username
    str[2]=u'密    码: '+ pwd
    fontsize = 19
    #fontname = u'Arial'
    hDC = win32ui.CreateDC() 
    hDC.CreatePrinterDC(win32print.GetDefaultPrinter()) 
    hDC.SetMapMode(4)
    font = win32ui.CreateFont({'name' : u'楷体_GB2312', 'height' : 22,'weight': True})
    hDC.SelectObject(font)
    hDC.StartDoc('untitled') 
    hDC.StartPage() 
    top = -5
    hDC.TextOut(fontsize,top,u'七天酒店欢迎您')
    font = win32ui.CreateFont({'name' : u'Arial', 'height' : 18,'weight': True})
    hDC.SelectObject(font)
    top=top-fontsize
    
    top = top - fontsize
    for t in str:
        #print t
        hDC.TextOut(fontsize,top,t)
        top = top - fontsize
        
    font = win32ui.CreateFont({'name' : u'Arial', 'height' : 16,'weight': True})
    hDC.SelectObject(font)
    fontsize=15
    str=[u'1.密码全部是小写字母',u'2.连接无线AP信号', u'3.打开浏览器,上网', u'4.访问任意网站',u'5.输入上面的用户名和密码',u'.']
    for t in str:
        #print t
        hDC.TextOut(fontsize,top,t)
        top = top - fontsize
    hDC.EndPage() 
    hDC.EndDoc() 
    

if __name__ == '__main__':
    reload(sys)
    print sys.getdefaultencoding()
    send_to_printer('&daysxxx','123','enuhvjqg')
    #prin t 'OK'
