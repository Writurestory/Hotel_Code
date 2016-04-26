#!/bin/bash

#安装wxpython的依赖
sudo apt-get install python-wxgtk2.8 python-wxtools python-wxversion
#安装目录
sudo cp ../sharedesktop  /usr/local/ -a
sudo chmod +x /usr/local/sharedesktop/horse
sudo chmod +x /usr/local/sharedesktop/blackhorse


sudo ln -s /usr/local/sharedesktop/horse  /usr/local/bin/horse
sudo ln -s /usr/local/sharedesktop/blackhorse  /usr/local/bin/blackhorse

echo "安装完成"

