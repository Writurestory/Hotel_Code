#!/usr/bin/env python
# -*- coding: utf-8-*-
import ConfigParser
def getconf():
    ret=[]
    config = ConfigParser.SafeConfigParser()
    config.read("conf.cfg")
    ret.append(config.get("linux", "multicastIP"))
    ret.append(config.get("linux", "port"))
    ret.append(config.get("linux", "ttl"))
    return ret
