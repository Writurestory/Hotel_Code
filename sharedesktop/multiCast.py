#!/usr/bin/env python

import socket
import struct
import scr
import Image,zlib,base64
import time
def main():
  MCAST_GRP = '224.1.1.1'
  MCAST_PORT = 9999
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
  while 1:
    time.sleep(0.1)
    w,h,t=scr.getdesktop()
    
    mesgLen=len(t)
    sendStart=0
    bufferSize=1280*8*20
    sendEnd=bufferSize
    #sc=0
    #ii=0
    
    try:
      sock.sendto('size:%d,%d,%d' %(w,h,mesgLen) ,(MCAST_GRP, MCAST_PORT))
      while sendStart<mesgLen:
        sendEnd=sendStart+bufferSize
        if sendEnd>mesgLen:sendEnd=mesgLen
        sd=zlib.compress(t[sendStart:sendEnd], zlib.Z_BEST_COMPRESSION)
        m=sock.sendto('img:%010d%010d:%s'%(sendStart,sendEnd,sd), (MCAST_GRP, MCAST_PORT))
        #m=sock.sendto('img:%010d%010d:%s'%(sendStart,sendEnd,sd), (MCAST_GRP, MCAST_PORT))
        print m
        sendStart=sendEnd
      #sock.sendto('EOF', (MCAST_GRP, MCAST_PORT))
      #m=sock.sendto('img:'+t[:60000], (MCAST_GRP, MCAST_PORT))
      #print "ssss",mesgLen/6
      #print "sendLen",m
      #ii+=1
      #print "ii=",ii
      #sc+=m-4
      #time.sleep(0.04)
      #print "s,e:",sendStart,sendEnd
        
    #time.sleep(1)
        #sock.sendto('EOF', (MCAST_GRP, MCAST_PORT))
    except Exception,e:
      print e
      
  #print "sc %d" %sc
  #print "MesgLen",mesgLen
  #print "messg",t[0:10],t[-10:]
  #im = Image.fromstring("RGB",[1280,800],zlib.decompress(base64.decodestring(t)))
  #im.show()
if __name__ == '__main__':
  main()
