# -*- coding: utf-8-*-
from distutils.core import setup
import py2exe

includes = ["conf","conf.cfg","hotelForm.xrc","left.jpg"]

options={"py2exe":{
    "dll_excludes": ["MSVCP90.dll"]
}}

setup(
#options=options,
zipfile=None,
windows=[{"script": "hotel.py", "icon_resources": [(1, "logo.ico")] }],
data_files=["conf.cfg","left.jpg","hotelForm.xrc","btlock55l.dll","logo.ico","mwic232.dll"],
version = "2013.1.11.01",   
description = "Network account Management",   
name = "NAM",
)  
