#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import string
import zlib,binascii
import struct
import wx

def Recv(_queue):
  MCAST_GRP = '224.1.1.1' 
  MCAST_PORT = 9999
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  try:
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
  except Exception,e:
    #print "dddddd",e
    pass
    
  
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
  sock.bind(('', MCAST_PORT))
  host=socket.gethostbyname(socket.gethostname())
  sock.setsockopt(socket.SOL_IP,socket.IP_MULTICAST_IF,socket.inet_aton(host))
  sock.setsockopt(socket.SOL_IP,socket.IP_ADD_MEMBERSHIP,socket.inet_aton(MCAST_GRP)+socket.inet_aton(host))
  
  while 1:
    try:
      data, addr = sock.recvfrom(1280*3*20*2+64)
      if data=='EOF':
        pass
      elif data[0:5]=='size:':
        w1,h1,s=data[5:].split(',')
        #w=string.atoi(w1)
        #h=string.atoi(h1)
      elif data[0:4]=='img:':
        #y=string.atoi(data[8:12])
        #imgList[y]=data[:]
        _queue.put(data[:])
        #print "sssssssssssssssssssssss"
        
      else:
	_queue.put(data[:])
        #print "-------------"

    except socket.error, e:
      print 'Expection:',e
      print "---------------"
  return 1280,800


    
if __name__ == '__main__':
  s=bytearray(1280*800*3)
  imgBuffer=buffer(s)
  imgList=[]
  Recv(imgList)
