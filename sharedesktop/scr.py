import gtk.gdk
import Image
import zlib,base64


def getdesktop():
    w = gtk.gdk.get_default_root_window()
    sz = w.get_size()
    print "The size of the window is %d x %d" % sz
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
    pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
    #pb=pb.scale_simple(800, 600,gtk.gdk.INTERP_TILES)
    if (pb != None):
        data=pb.get_pixels()
        print "orign",len(data)
        #d1=base64.encodestring(zlib.compress(data, zlib.Z_BEST_COMPRESSION))
        d2=zlib.compress(data, zlib.Z_BEST_COMPRESSION)
        #print "d1,d2",len(d1),len(d2)
        print "d2:",len(d2)
        #print len(d2)
        #pb.save("screenshot.png","png")
        #print d2
        return [sz[0],sz[1],data]
    #w=pb.get_width()
    #h=pb.get_height()
    #print w
    #im = Image.fromstring("RGB",[w,h],data)
    #print im.size
        
    #im.show()
    #tim=im.tostring()
    #print len(tim)
    #tim=im.tostring("jpeg","")
    #print tim.info
    #pb.save("screenshot.png","png")
        print "Screenshot saved to screenshot.png."
    else:
        print "Unable to get the screenshot."
        return ''
        
if __name__ == '__main__':
  getdesktop()
