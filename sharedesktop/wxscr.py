#!/user/bin/env python
# -*- coding: utf-8-*-
import wx,signal,sys
import zlib
import socket,time
import Image
import struct,hashlib
import myconf,string


global sock
global send_flag
global MCAST_GRP, MCAST_PORT
def getImgPix(src_x,src_y,w,h):
    #wx.App()  # Need to create an App instance before doing anything
    screen = wx.ScreenDC()
    size = screen.GetSize()
    bmp = wx.EmptyBitmap(w,h)
    mem = wx.MemoryDC(bmp)
    mem.Blit(0, 0,w,h, screen, src_x,src_y)
    data=buffer(bytearray(w*h*3))
    bmp.CopyToBuffer(data)
    rt =zlib.compress(data, zlib.Z_BEST_COMPRESSION)
    return rt

def ScreenImgSend():
    global sock
    global send_flag
    global MCAST_GRP, MCAST_PORT
    cfg=myconf.getconf()
    MCAST_GRP = cfg[0]
    MCAST_PORT = string.atoi(cfg[1])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, string.atoi(cfg[2]))
    screen = wx.ScreenDC()
    size = screen.GetSize()
    y_axis=0
    height_step=20
    cursorIndex=0
    while send_flag:
        try:
            time.sleep(0.02)
            imgBuff=getImgPix(0,y_axis,size[0],height_step)
            curp = wx.GetMousePosition()
            pos="%04d%04d%04d%04d%04d%04d" %(0,y_axis,size[0],height_step,curp[0],curp[1])
            m=sock.sendto('img:%s:%s'%(pos,imgBuff), (MCAST_GRP, MCAST_PORT))
            #print len(imgBuff)
            y_axis+=height_step
            if y_axis==size[1]:
                y_axis=0
            elif y_axis+height_step > size[1]:
                y_axis=size[1]-height_step
        except Exception,e:
            print e
def sigint_handler(signum,frame):    
    global sock
    global send_flag
    global MCAST_GRP, MCAST_PORT
    send_flag=False
    print "\nstop to send screen"  
    for t in range(1,10):
        #send close signal to client
        m=sock.sendto('ctl:close', (MCAST_GRP, MCAST_PORT))
        time.sleep(0.03)
    
    sys.exit()

if __name__ == '__main__':    
    global send_flag
    send_flag=True
    app=wx.App()
    signal.signal(signal.SIGINT,sigint_handler)
    print "Ctrl-C to terminate"

    ScreenImgSend()
    app.MainLoop()

